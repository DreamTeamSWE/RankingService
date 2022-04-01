import boto3


class Database:
    AWS_KEY = 'AKIARZPP2F6H24B5GXVA'
    AWS_PSW = 'P61Tdsg5C4mg72PjhPULTFa9dqz0pt5hWRt+K815'
    AWS_REGION = 'eu-central-1'

    def __init__(self, database: str) -> None:
        self.__rdsData = boto3.client('rds-data', region_name=self.AWS_REGION, aws_access_key_id=self.AWS_KEY,
                                      aws_secret_access_key=self.AWS_PSW)
        self.__cluster_arn = 'arn:aws:rds:eu-central-1:123446374287:cluster:sweeat'
        self.__secret_arn = 'arn:aws:secretsmanager:eu-central-1:123446374287:secret:rds-db-credentials/cluster' \
                            '-AQLMTHUP2LEAFVXYXDMZFEHDR4/admin-5WXjei '
        self.__database = database

    def __parse_result(self, results):
        columns = [column['name'] for column in results['columnMetadata']]
        parsed_records = []
        for record in results['records']:
            parsed_record = {}
            for i, cell in enumerate(record):
                key = columns[i]
                value = list(cell.values())[0]
                parsed_record[key] = value
            parsed_records.append(parsed_record)
        return parsed_records

    # param_set format: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html
    # #RDSDataService.Client.execute_statement
    def do_write_query(self, query: str, param_set=None):
        if param_set is None:
            param_set = []
        response = self.__rdsData.execute_statement(resourceArn=self.__cluster_arn,
                                                    secretArn=self.__secret_arn,
                                                    database=self.__database,
                                                    sql=query,
                                                    parameters=param_set)
        return response

    # param_set format: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html
    # #RDSDataService.Client.execute_statement
    def do_read_query(self, query: str, param_set=None):
        if param_set is None:
            param_set = []
        response = self.__rdsData.execute_statement(resourceArn=self.__cluster_arn,
                                                    secretArn=self.__secret_arn,
                                                    database=self.__database,
                                                    sql=query,
                                                    parameters=param_set,
                                                    includeResultMetadata=True)
        return self.__parse_result(response)
