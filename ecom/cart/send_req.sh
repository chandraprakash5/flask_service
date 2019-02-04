#!/bin/bash

DECLAYER_API_KEY=XUAWYHlh8g
VALUES_FILE_PATH=$1
application_id=$(grep -i 'application_id:' $VALUES_FILE_PATH | awk '{print $2}' | tr -d '\r')
echo $application_id
value=$(cat $VALUES_FILE_PATH | gzip | base64)
commit_id=$(git log --format="%H" -n 1)
image_tag=$commit_id
last_commit_author=$(git log -1 --pretty=format:'%an')
last_commit_email=$(git log -1 --pretty=format:'%ae')
last_commit_epoch_time_sec=$(git log -1 --pretty=format:'%ct')
last_commit_subject=$(git log -1 --pretty=format:'%s' | gzip | base64)
last_commit_branch=$(git rev-parse --abbrev-ref HEAD)
commit_info='{"author":"'$last_commit_author'","email":"'$last_commit_email'","timestamp":"'$last_commit_epoch_time_sec'","subject_gz_b64":"'$last_commit_subject'","branch":"'$last_commit_branch'"}'
commit_info=$(echo $commit_info | gzip | base64)
values='{"value_gz_b64":"'"$value"'","commit_id":"'"$commit_id"'","application_id":"'"$application_id"'","image_tag":"'"$image_tag"'","commit_info_gz_b64":"'"$commit_info"'"}'
mkdir -p /tmp/$application_id/
echo $values > /tmp/$application_id/$commit_id
curl -v -i http://13.233.82.112:3000/v1/update -H "Authorization: DECL_API_KEY apikey=$DECLAYER_API_KEY" -H 'content-type: application/json' --data @/tmp/$application_id/$commit_id
rm -rf /tmp/$application_id
