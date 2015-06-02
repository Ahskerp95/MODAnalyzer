#include <iostream>
#include <vector>
#include <unordered_map>
#include <exception>
#include <fstream>
#include <memory>
#include <string>
#include <iomanip> 

#include "../interface/event.h"

using namespace std;
using namespace fastjet;


MODEvent::MODEvent(int run_number, int MODEvent_number) : _run_number(run_number), _event_number(MODEvent_number) {}

MODEvent::MODEvent() {}

int MODEvent::event_number() {
	return _event_number;
}

int MODEvent::run_number() {
	return _run_number;
}


void MODEvent::set_run_number(int run_number) {
	_run_number = run_number;
}

void MODEvent::set_particles_trigger_type(string trigger_type) {
	_trigger_type = trigger_type;
}

void MODEvent::set_event_number(int event_number) {
	_event_number = event_number;
}




vector<PseudoJet> MODEvent::particles_four_vectors() {
	vector<PseudoJet> four_vectors;
	for (unsigned int i = 0; i < _particles.size(); i++) {
		four_vectors.push_back(_particles[i].four_vector());
	}

	return four_vectors;
}

vector<MODParticle> MODEvent::particles() {
	return _particles;
}

void MODEvent::add_particle(string input_string) {
	_particles.push_back(MODParticle(input_string));
}

void MODEvent::add_trigger(string input_string) {
	_triggers.push_back(MODTrigger(input_string));
}

MODTrigger MODEvent::trigger_by_name(string name) {
	vector<MODTrigger> triggers = this->triggers();

	for(int i = 0; i < triggers.size(); i++) {
		MODTrigger current_trigger = triggers[i];

		if (current_trigger.name() == name) {
			return current_trigger;
		}
	}

	MODTrigger * empty_trigger = new MODTrigger();
	return * empty_trigger;
}

vector<MODTrigger> MODEvent::triggers() {
	return _triggers;
}

void MODEvent::write_to_file(string filename) {
	ofstream file_to_write;
	file_to_write.open( filename, ios::out | ios::app ); 

	file_to_write << "BeginEvent Run " << _run_number << " Event " << _event_number << endl;
	
	// First, write out all particles.

	file_to_write << _particles[0].header();
	for (int i = 0; i < _particles.size(); i++) {
		file_to_write << _particles[i].make_string();
	}

	// Next, write out all triggers.

	file_to_write << _triggers[0].header();
	for(int i = 0; i < _triggers.size(); i++) {
		file_to_write << _triggers[i].make_string();
	}

	file_to_write << "EndEvent" << endl;
}

double MODEvent::hardest_pt() {
	vector<PseudoJet> particles = this->particles_four_vectors();

	// Run the clustering, extract the jets using fastjet.
	JetDefinition jet_def(antikt_algorithm, 0.5);
	ClusterSequence cs(particles, jet_def);
	vector<PseudoJet> clustered_jets = cs.inclusive_jets(0.0);

	double hardest_pt = 0.0;
	for (unsigned int i = 0; i < clustered_jets.size(); i++) {
		if (hardest_pt < clustered_jets[i].pt()) {
			hardest_pt = clustered_jets[i].pt();
		}
	}

	return hardest_pt;
}

string MODEvent::assigned_trigger_name() {

	double hardest_pt = this->hardest_pt();

	// Next, lookup which trigger to use based on the pt value of the hardest jet.

	string trigger_to_use;
	if (hardest_pt > 153) {
		trigger_to_use = "HLT_Jet70U";
	}
	else if (hardest_pt > 114) {
		trigger_to_use = "HLT_Jet50U";
	}
	else if (hardest_pt > 84) {
		trigger_to_use = "HLT_Jet30U";
	}
	else if (hardest_pt > 56) {
		trigger_to_use = "HLT_Jet15U";
	}
	else if (hardest_pt > 37) {
		trigger_to_use = "HLT_L1Jet6U";
	}
	else {
		trigger_to_use = "HLT_MinBiasPixel_SingleTrack";
	}
	
	// Here, we just return the trigger that was supposed to fire, not caring whether it actually did or not.
	// A check on whether it actually fired or not will be done in the analysis.cc file itself.

	return trigger_to_use;
}