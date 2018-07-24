#!/bin/sh
# Cross_Initialize

# Full path to script location no matter where it is called from
current=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )

# Empty String
inputstring=""

#Accept Arguments
while [[ "$#" > 1 ]]; do case $1 in # While there are more than 1 argument
    --config) CONFIG_FILE="$2";; # if $1 matches "--config", set $2 to "CONFIG_FILE"
    --subject) subject_id="$2";;
    --timepoint) timepoint="$2";;
    --inputfile) inputstring="${inputstring} -i $2";;
    *);; # if $1 does not match any of the four things above, keep looking for a match 
  esac; shift # Shift removes arguments in beggning of the argument list (Makes #2 --> $1)
done

if [[ x${CONFIG_FILE} == x ]] ; then # Checks if "CONFIG_FILE" is empty same thing as [ -z "${CONFIG_FILE"} ]
  echo "CONFIG_FILE is not defined!"
  exit 0 # exit code 0 means "success"
fi

source ${CONFIG_FILE} # source executes the content of the file passed as argument

if [[ x${FREESURFER_HOME} == x ]] ; then
  echo "FREESURFER_HOME is not defined!"
  exit 1 # exit code 1 means "errors or failure"
fi

if [[ x${SUBJECTS_DIR} == x ]] ; then
  echo "SUBJECTS_DIR is not defined!"
  exit 1
fi

if [[ x${MONITOR_DIR} == x ]] ; then
  echo "MONITOR_DIR is not defined!"
  exit 1
fi

export FREESURFER_HOME=$FREESURFER_HOME # export exports a variable to the enviornment to any child process runing in current shell
export SUBJECTS_DIR=$SUBJECTS_DIR

source ${FREESURFER_HOME}/SetUpFreeSurfer.sh

if [[ ${IS_LONGITUDINAL} == True ]] ; then
  echo "Longitudinal Processing"
  if [[ x${timepoint} == x ]] ; then
    echo "No timepoint specified!"
    exit 1
  else
    subject_id=${subject_id}_${timepoint}
  fi
fi
echo $subject_id

#Create the row
${current}/palantir/palantir update ${MONITOR_DIR} --addrow ${subject_id}
${current}/palantir/palantir cell ${MONITOR_DIR} -r ${subject_id} -c Extract --settext "N/A" --setbgcolor "#d2d2d2" --settxtcolor "#f0f0f0" --setbool "False"

#Set to running
${current}/palantir/palantir cell ${MONITOR_DIR} -r ${subject_id} -c Cross_Initialize --settext "Running" --setanimate "bars" --setbgcolor "#efd252" --settxtcolor "#ec6527" --addnote "Started running"

if [ $HOSTNAME != $DESIRED_HOSTNAME ] ; then
  echo "ERROR: NOT ON CORRECT HOST FOR RUNNING FREESURFER"
  echo "ABORTING PROCESS"
  ${current}/palantir/palantir cell ${MONITOR_DIR} -r ${subject_id} -c Cross_Initialize --settext "Host Error" --setanimate "toggle" --setbgcolor "#cb3448" --settxtcolor "#791f2b"
  exit 1
fi

if recon-all ${inputstring} -subjid ${subject_id} -all ; then
  ${current}/palantir/palantir cell ${MONITOR_DIR} -r ${subject_id} -c Cross_Initialize --settext "Finished" --setanimate "none" --setbgcolor "#009933" --settxtcolor "#004c19" --addnote "Successfully finished"
else
  ${current}/palantir/palantir cell ${MONITOR_DIR} -r ${subject_id} -c Cross_Initialize --settext "Error" --setanimate "toggle" --setbgcolor "#cb3448" --settxtcolor "#791f2b" --addnote "Error"
  exit 1
fi

exit 0
