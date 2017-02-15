
''' dtiFit.py
# CCNC DTI FA map
# Created by Eunseo Cho
# 2017.02.10 - 2017.02.15
'''
import re
import os
import argparse
import textwrap
import glob
from progressbar import AnimatedMarker, ProgressBar, Percentage, Bar


def dtiFit(dtidir):
	'''
	Searching DTI data 

	'''	
	dti_source_directory = os.path.join(dtidir)
	print '\n' + dti_source_directory + '\n'

	if re.search('nii.gz$', ' '.join(os.listdir(dtidir))):
		files = os.listdir(dti_source_directory)
	else:
		print 'There are no dti data'

	#print files

	dtiData = files[3]
	print '\n' + dtiData + '\n'

	# B0 extraction from data	
	print '='*80, '\nB0 extraction from data\n', '='*80

	command = 'fslroi {inDtiImage} {outDtiImage} {tmin} {tsize}'.format(
						   inDtiImage=os.path.join(dti_source_directory,dtiData),
						   outDtiImage=os.path.join(dti_source_directory, 'b0.nii.gz'),
						   tmin=0,
						   tsize=1)	
	print '-'*80, '\n', re.sub('\s+', ' ', command), '\n', '-'*80
	pbar = ProgressBar().start()
	output = os.popen(command).read()
	pbar.finish()


	# Brain extraction
	print '='*80, '\nBrain extraction\n', '='*80

	command = 'bet {inBetImage} {outBetImage} -m -f {threshold}'.format(
						inBetImage=os.path.join(dti_source_directory,'b0.nii.gz'),
						outBetImage=os.path.join(dti_source_directory, 'b0_brain.nii.gz'),
						threshold=0.35)

	print '-'*80, '\n', re.sub('\s+', ' ', command), '\n', '-'*80
	pbar = ProgressBar().start()
	output = os.popen(command).read()
	pbar.finish()
	

	# Eddy current correction
	print '='*80, '\nEddy current correction\n', '='*80

	command = 'eddy_correct {inDtiImage} {eddyDtiImage} {referenceNum}'.format(
								inDtiImage=os.path.join(dti_source_directory,dtiData),
								eddyDtiImage=os.path.join(dti_source_directory, 'eddy_data.nii.gz'),
								referenceNum=0)

	print '-'*80, '\n', re.sub('\s+', ' ', command), '\n', '-'*80
	pbar = ProgressBar().start()
	output = os.popen(command).read()
	pbar.finish()


	# Fitting a tensor
	print '='*80, '\nFitting a tensor\n', '='*80
	command = 'dtifit -k {eddyDtiImage} -o {basename} -m {mask} -r {bvecs} -b {bvals}'.format(
							  eddyDtiImage=os.path.join(dti_source_directory,'eddy_data'),
							  basename=os.path.join(dti_source_directory,'DTI'),
							  mask=os.path.join(dti_source_directory, 'b0_brain_mask'),
							  bvecs=os.path.join(dti_source_directory, "*.bvec"),
							  bvals=os.path.join(dti_source_directory, '*.bval'))
	
	print '-'*80, '\n', re.sub('\s+', ' ', command), '\n', '-'*80
	pbar = ProgressBar().start()
	output = os.popen(command).read()
	pbar.finish()


def main(dtidir):
	
	dtiFit(dtidir)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
            description = textwrap.dedent('''\
                    {codeName} : DTI FA Map
                    ====================
                        eg) {codeName}
                    '''.format(codeName=os.path.basename(__file__))))
	
	parser.add_argument(
        '-d', '--dtidir',
        help='DTI data directory location, default = my dti',
        action='store_true',
        default="/Users/bienseo/Desktop/DTI") #default=os.getcwd())

	args = parser.parse_args()
 	
 	main(args.dtidir)
 '''
 import to backUp.py 
 '''	
