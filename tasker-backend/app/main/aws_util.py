from ssm_parameter_store import EC2ParameterStore

# get access id and secert from aws to run on local
aws_param_store = EC2ParameterStore(aws_access_key_id="AKIAUU63GJAHLC5EZANZ",
                                    aws_secret_access_key="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",
                                    region_name='ap-south-1')

google_app_credentials = aws_param_store.get_parameters_with_hierarchy(
    "/applications/google/places")
