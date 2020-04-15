mkdir -p lambda_layer/python/lib/python3.7/site-packages
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate
pip install -r fred_data_layer_requirements.txt -t lambda_layer/python/lib/python3.7/site-packages
cd lambda_layer/python/lib/python3.7/site-packages
wget https://github.com/cgroll/data_apps_aws/archive/master.zip
unzip master.zip
rm master.zip

# TODO: get data_apps_aws out from data_apps_aws-master folder
# rm data_apps_aws-master folder

cd ../../../../
zip -r fred_data_pipe_layer.zip python

# Upload to S3
# create new layer (version) from S3 file

