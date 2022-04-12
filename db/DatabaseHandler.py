import time
import boto3
import logging
from botocore.exceptions import ClientError


class DatabaseHandler:
    AWS_REGION = 'eu-central-1'

    def __init__(self, database: str) -> None:
        self.__rdsData = boto3.client('rds-data', region_name=self.AWS_REGION)
        self.__cluster_arn = 'arn:aws:rds:eu-central-1:123446374287:cluster:sweeat'
        self.__secret_arn = 'arn:aws:secretsmanager:eu-central-1:123446374287:secret:rds-db-credentials/cluster' \
                            '-AQLMTHUP2LEAFVXYXDMZFEHDR4/admin-5WXjei'
        self.__database = database
        self.__wait_for_db_on()

    # check if db is turned on
    def __is_db_on(self, delay) -> bool:
        """
        Check if database is turned on.

        :type delay: int
        :param delay: delay between checks
        :return: boolean if db is on
        """
        try:
            self.__rdsData.execute_statement(resourceArn=self.__cluster_arn,
                                             secretArn=self.__secret_arn,
                                             database=self.__database,
                                             sql='SELECT 1',
                                             parameters=[],
                                             includeResultMetadata=True)
            return True
        except ClientError as ce:
            error_code = ce.response.get("Error").get('Code')
            error_msg = ce.response.get("Error").get('Message')

            # Aurora serverless is waking up
            if error_code == 'BadRequestException' and 'Communications link failure' in error_msg:
                logging.info('Sleeping ' + str(delay) + ' secs, waiting DB connection')
                time.sleep(delay)
                return False
            else:
                raise ce

    # for two minutes check if db is on
    def __wait_for_db_on(self):
        """
        Wait for database to be turned on.
        """
        ok = False
        for i in range(20):
            ok = self.__is_db_on(10)
            if ok is True:
                logging.info('DB is on')
                return
        if ok is False:
            logging.info('cannot connect to DB')

    @staticmethod
    def __parse_result(results):
        """
        Parse result from RDS Data API.

        :param results: result from RDS Data API

        :rtype: list
        :return: parsed result
        """
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

    @staticmethod
    def __add_null_values(param_list):
        def __add_null_values(param_list):
            key = [*param_list['value']][0]
            if param_list['value'][key] is None:
                del param_list['value'][key]
                param_list['value']['isNull'] = True


    def begin_transaction(self):
        """
        Begin transaction.

        :return: transaction id
        """
        response = self.__rdsData.begin_transaction(resourceArn=self.__cluster_arn,
                                                    secretArn=self.__secret_arn,
                                                    database=self.__database)
        return response['transactionId']

    def commit_transaction(self, transaction_id):
        """
        Commit transaction.

        :param transaction_id:
        :return: response of query
        """
        response = self.__rdsData.commit_transaction(resourceArn=self.__cluster_arn,
                                                     secretArn=self.__secret_arn,
                                                     transactionId=transaction_id)
        return response

    # param_set format: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html
    # #RDSDataService.Client.execute_statement
    def do_write_query(self, query: str, param_set=None, transaction_id=None):
        """
        Execute write query.

        :param query: query to execute
        :param param_set: parameters for query
        :param transaction_id: transaction id

        :rtype: dict
        :return: response of query
        """
        if param_set is None:
            param_set = []
        if transaction_id is not None:
            response = self.__rdsData.execute_statement(resourceArn=self.__cluster_arn,
                                                        secretArn=self.__secret_arn,
                                                        database=self.__database,
                                                        sql=query,
                                                        parameters=param_set,
                                                        transactionId=transaction_id)
        else:
            response = self.__rdsData.execute_statement(resourceArn=self.__cluster_arn,
                                                        secretArn=self.__secret_arn,
                                                        database=self.__database,
                                                        sql=query,
                                                        parameters=param_set)
        return response

    # param_set format: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html
    # #RDSDataService.Client.execute_statement
    def do_read_query(self, query: str, param_set=None, transaction_id=None):
        """
        Execute read query.

        :param query: query to execute
        :param param_set: parameters for query
        :param transaction_id: transaction id

        :rtype: dict
        :return:
        """
        if param_set is None:
            param_set = []
        if transaction_id is not None:
            response = self.__rdsData.execute_statement(resourceArn=self.__cluster_arn,
                                                        secretArn=self.__secret_arn,
                                                        database=self.__database,
                                                        sql=query,
                                                        parameters=param_set,
                                                        includeResultMetadata=True,
                                                        transactionId=transaction_id)
        else:
            response = self.__rdsData.execute_statement(resourceArn=self.__cluster_arn,
                                                        secretArn=self.__secret_arn,
                                                        database=self.__database,
                                                        sql=query,
                                                        parameters=param_set,
                                                        includeResultMetadata=True)
        return self.__parse_result(response)
