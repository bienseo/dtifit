
'''
# CCNC DTI FA map
# Created by Eunseo Cho
# 2017.02.10 - 
'''
import re
import os
import argparse
import textwrap


def dtifit(dtidir):
	
	dtiData = 'data.nii.gz'

	# B0 extraction from data
	print '='*80, '\nB0 extraction from data\n', '='*80

	command = 'fslroi {inDtiImage} {outDtiImage} {tmin} {tsize}'.format(
					   inDtiImage=os.path.join(dtidir,dtiData),
					   outDtiImage=os.path.join(dtidir, 'b0.nii.gz'),
					   tmin=32,
					   tsize=1)

	print '-'*80, '\n', re.sub('\s+', ' ', command), '\n', '-'*80
	output = os.popen(command).read()

	#Brain extraction
	print '='*80, '\nBrain extraction\n', '='*80

	command = 'bet {inBetImage} {outBetImage} -m -f {threshold}'.format(
					inBetImage=os.path.join(dtidir,'b0.nii.gz'),
					outBetImage=os.path.join(dtidir, 'b0_brain.nii.gz'),
					threshold=0.35)

	print '-'*80, '\n', re.sub('\s+', ' ', command), '\n', '-'*80
	output = os.popen(command).read()

	# Eddy current correction
	print '='*80, '\nEddy current correction\n', '='*80

	command = 'eddy_correct {inDtiImage} {eddyDtiImage} {referenceNum}'.format(
							inDtiImage=os.path.join(dtidir,dtiData),
							eddyDtiImage=os.path.join(dtidir, 'eddy_data.nii.gz'),
							referenceNum=32)

	print '-'*80, '\n', re.sub('\s+', ' ', command), '\n', '-'*80
	output = os.popen(command).read()

	# Fitting a tensor
	print '='*80, '\nFitting a tensor\n', '='*80

	command = 'dtifit -k {eddyDtiImage} -o {basename} -m {mask} -r {bvecs} -b {bvals}'.format(
						  eddyDtiImage=os.path.join(dtidir,'eddy_data'),
						  basename=os.path.join(dtidir,'DTI'),
						  mask=os.path.join(dtidir, 'b0_brain_mask'),
						  bvecs=os.path.join(dtidir, 'subj.bvecs'),
						  bvals=os.path.join(dtidir, 'subj.bvals'))

	print '-'*80, '\n', re.sub('\s+', ' ', command), '\n', '-'*80
	output = os.popen(command).read()


def main(dtidir):
	
	dtifit(dtidir)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
            description = textwrap.dedent('''\
                    {codeName} : DTI FA Map
                    ====================
                        eg) {codeName}
                    '''.format(codeName=os.path.basename(__file__))))
	
	parser.add_argument(
        '-dd', '--dtidir',
        help='DTI data directory location, default = my dti',
        action='store_true',
        default="/Users/bienseo/Desktop/SNU_CCNC/FSL_prac/subj02/DTI") #default=os.getcwd())

	args = parser.parse_args()
 	
 	main(args.dtidir)


