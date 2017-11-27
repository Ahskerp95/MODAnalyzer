from __future__ import division
import sys
import os
import shutil

move_from = sys.argv[1]
move_to = sys.argv[2]


names = ["E295FFD7-B171-E011-AA8F-00266CF327C0.mod", "D4F0E262-9271-E011-BF37-0025901D4D64.mod", "F672CE54-1B71-E011-93CD-003048D439AC.mod", "EEED891A-0E71-E011-8E23-003048C693F0.mod", "E88291AB-4F71-E011-A210-003048CF6336.mod", "E03D8DFB-F670-E011-BEC9-003048CF6334.mod", "F2A6C3C3-5471-E011-B36E-003048F0E822.mod", "E2EF9E33-6271-E011-9A6A-003048D4390A.mod", "E41464FB-2671-E011-B4B2-003048F0E824.mod", "DA6127AC-7471-E011-AEA8-003048D462C8.mod", "E6A5B9E3-8771-E011-BDE8-002481E0E912.mod", "E4C3F1FA-0371-E011-86DB-0025901D47AA.mod", "FA5CFAA6-4F71-E011-A7D8-002481E0D448.mod", "F23F1734-AC71-E011-9672-003048D462DC.mod", "CC4992A4-6E71-E011-9005-00266CF327C4.mod", "FAF89C83-3E71-E011-93BC-00266CF2AACC.mod", "F845640A-9B71-E011-AD94-0025901D4938.mod", "F46EF9E4-8871-E011-AF60-003048C68A98.mod", "F036B461-0B71-E011-B204-0025901D4D6C.mod", "DCA83164-837A-E011-9736-0025901D4138.mod", "FC6B0483-F470-E011-AF8F-0025901D40CA.mod", "EA1DE1DB-9171-E011-A4FB-0025901D4D54.mod", "E6FFE975-2571-E011-9E0F-003048F0E186.mod", "E015C7F5-EF70-E011-BD8B-003048C69040.mod", "EE96816B-7171-E011-A7B9-003048D438FE.mod", "E4A8EC4A-3D71-E011-A344-003048D43838.mod", "FA7AB82B-6271-E011-9B0C-003048D43726.mod", "FE2FD28F-AD71-E011-9302-00237DDC5E96.mod", "D0FB54E7-0371-E011-A0C3-003048D43942.mod", "EEDF9A47-BF71-E011-A5A7-00266CF25320.mod", "FC2D1A92-A871-E011-BE0A-002481E0DDBE.mod", "E0A5A818-A671-E011-B034-003048D437BA.mod", "EA03AEF0-9771-E011-ABE1-003048D3C8FC.mod", "E029A937-2671-E011-A94F-003048D439B6.mod", "E879016B-3371-E011-B640-00266CF32D24.mod", "E03268AA-4F71-E011-8D6D-003048D4DFB8.mod", "F03E0813-5871-E011-9726-003048F0E828.mod", "E6D5A292-B071-E011-82D4-002481E15204.mod", "F492E93A-1F71-E011-AAB0-00266CF32FA0.mod", "E0471418-8A71-E011-9199-003048C692D6.mod", "FCE10B42-3A71-E011-A007-00266CF33054.mod", "FAF405A4-8B71-E011-8359-003048D43994.mod", "E8027E28-6671-E011-B6BF-003048D437F2.mod", "F6A51BE4-F770-E011-8D37-003048D4DFA4.mod", "EC2F13BC-2571-E011-AA56-003048F0E194.mod", "E4CCC911-B171-E011-A7DF-003048F02CBE.mod", "E8E942EC-3771-E011-A761-00266CF32930.mod", "E6F8C1BD-EE70-E011-B344-003048D439AA.mod", "F24988B9-8871-E011-BEC8-0025901D4D6C.mod", "E825163A-4471-E011-B3BD-003048F0E184.mod", "E099CB12-C771-E011-BAC8-002481E0DBE0.mod", "E6401950-0371-E011-A53E-0025901D47AA.mod", "F89C2598-0471-E011-93A0-003048D43656.mod", "E691A649-2B71-E011-8808-003048F0E526.mod", "FC78CB27-FE70-E011-986C-003048D4797E.mod", "E0C96D2E-B171-E011-B17A-003048D3C7DC.mod", "FCDD3E00-B171-E011-AF78-002481E94C56.mod", "EC24AC1D-4F71-E011-A757-003048D373CC.mod", "E855678F-2771-E011-9E79-00266CF32EB8.mod", "EAD0B63F-5071-E011-BC11-003048F0E83A.mod", "E2FDF6CB-3671-E011-B52E-003048D43986.mod", "EEF5584B-8D71-E011-B8E5-0025901D4B04.mod", "E6CCB824-957A-E011-9C7E-003048CFCBB2.mod", "2E90EE96-F570-E011-8254-003048C6928C.mod", "E6828D2B-6271-E011-89FA-003048C693DA.mod", "F8ED6A8A-AD71-E011-91AF-002481E0EA70.mod", "F2CE4CD6-5471-E011-986A-002481E0D974.mod", "F2C936A5-1674-E011-AC3F-003048F0E3AE.mod", "F0DADA21-FE70-E011-BF21-003048D3CB3C.mod", "EEABAAE9-9171-E011-8E5B-0025901D40CA.mod", "E60AAB1F-3771-E011-9B3F-002481E0D974.mod", "FA94AEFE-B071-E011-9385-002481E94BCA.mod", "FA2F4163-9271-E011-8702-003048C68A90.mod", "E667FDB0-2371-E011-9FA3-00266CF2AE10.mod", "F08C8E9D-6271-E011-89C8-003048D43726.mod", "EA50153B-2671-E011-B9DF-003048D4399E.mod", "DE45EA12-C271-E011-85D2-003048D4DEBC.mod", "C6751369-AD71-E011-8A24-003048D4385C.mod", "EE8E7B62-667A-E011-84DA-0030487E54B7.mod", "F696E033-C971-E011-B0FE-003048CFCBB0.mod", "E84B88EA-6471-E011-953E-002481E0D678.mod", "F0BD04E2-1C71-E011-94FA-00266CF32F00.mod", "DCF2C83C-0071-E011-8103-002481E0D5E2.mod", "0ED4517A-7C7A-E011-934A-003048C69032.mod", "E88748FD-3771-E011-BB84-003048D4DFA8.mod", "EAE4F1D8-EF70-E011-ACD7-003048D4399E.mod", "FA348FE6-FD70-E011-BE62-003048D3C886.mod", "DEEF1F0C-C671-E011-80E8-003048F0E3D0.mod", "F240D12C-1C71-E011-9722-002481E945C4.mod", "2E89F45E-B071-E011-9038-003048C693E2.mod", "DE4FEB50-6571-E011-8E99-003048C693D2.mod"]

def move_files(move_from, move_to):
	
	
	for f in os.listdir(move_from):
		if f in names:
			# shutil.copy(move_from + "/" + f, move_to + "/" + f)
			os.rename(move_from + "/" + f, move_to + "/" + f)

	


move_files(move_from, move_to)