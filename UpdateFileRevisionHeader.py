import os
import string
import re

origDir = os.getcwd()
newDir = os.path.join(origDir, "new")

# Check if a "new" directory already exists, if so then remove the files 
# currently in it.  If it doesn't exist, then create it.
if (os.path.exists(newDir)):
   for file in os.listdir(newDir):
      os.remove(os.path.join(newDir, file))
else:
   os.mkdir(newDir)

# Check each file in the current directory
for file in os.listdir(origDir):
   
   # Test type 1 - batch files:
   if file.endswith("bat"):
      
      # Check if the file has already been updated.  To do so, read the first
      # line of the file, and check if it matches "set Revision Revision"
      origFile = open(file,'r')
      if (origFile.readline() != "set Revision Revision\n"):
         
         # File needs to be updated, set the first two lines
         contents = []
         contents.append("set Revision Revision\n")
         contents.append("set rev \"$Revision$\"\n")
         
         # Loop through each line of the file
         for x in origFile.readlines():
            
            # Replace the line containing the old Log keyword, with the 
            # sequence to achieve both Starteam and MKS histories
            if re.search("\$Log", x):
               contents.append("## Starteam:\n")
               contents.append("##   $Log:\n")
               contents.append("##   $\n")
               contents.append("##   $NoKeywords$\n")
               contents.append("##\n")
               contents.append("## MKS:\n")
               contents.append("##   $Log$\n")
            
            # Replace the old line that reported the version number with the
            # new method
            elif re.search("TEST_NAME.bat", x):
               contents.append("putres \"## $TEST_NAME.bat: $rev\"\n")
            
            # Leave all other lines alone
            else:
               contents.append(x)
         
         origFile.close()
         
         # Create the new file and write the contents
         os.chdir(newDir)
         newFile = open(file, 'w')
         newFile.writelines(contents)
         newFile.close()
         
         os.chdir(origDir)
   
   # Test type 2 - c files:
   elif file.endswith(".c"):
   
      # Check if the file has already been updated.  To do so, read the entire
      # contents of the file and check if NoKeywords is present
      origFile = open(file,'r')
      x = origFile.read()
      if (x.find("NoKeywords") < 0):
         
         # File needs to be updated.  Need to re-read it.
         contents = []
         origFile = open(file,'r')
         
         # Loop through each line of the file
         for x in origFile.readlines():
            
            # Replace the line containing the old Log keyword, with the 
            # sequence to achieve both Starteam and MKS histories
            if re.search("\$Log", x):
               contents.append("** Starteam:\n")
               contents.append("**   $Log:\n")
               contents.append("**   $\n")
               contents.append("**   $NoKeywords$\n")
               contents.append("**\n")
               contents.append("** MKS:\n")
               contents.append("**   $Log$\n")
            
            # Leave all other lines alone
            else:
               contents.append(x)
         
         origFile.close()
         
         # Create the new file and write the contents
         os.chdir(newDir)
         newFile = open(file, 'w')
         newFile.writelines(contents)
         newFile.close()
         
         os.chdir(origDir)
   
