from analyzer.PostAnalyzer import PostAnalyzer
import FacadeAnalyzePost
import json
from entity.CrawledData import CrawledData
from entity.Restaurant import Restaurant
from entity.Filter import Filter
from db.RepositoryExternal import RepositoryExternal

if __name__ == '__main__':
    # str = (
    #     "Sarde al beccafico, pani e panelle, ventresche al carbone, polli farciti alla grande e una girandola senza "
    #     "fine di dessert: Ciccio Sultano e Fabrizio Fiorani hanno scosso Via Veneto a Roma con mitragliate di cucina "
    #     "siciliana e confesso che si è goduto \r\n.\r\n@giano.restaurant al @w_romehotel \r\n.\r\n👉link in bio")
    #
    # data = CrawledData(
    #     caption=str, image=None, restaurant=Restaurant("Da ciccio")
    # )
    #
    # FacadeAnalyzePost.refresh_ranking(
    #     post=data,
    #     analyzer=PostAnalyzer(),
    #     repository=None)

    filter = Filter("text", "10", "kebab", 10, 5)
    print(filter.make_query())

    print('Done')


def lambda_handler(event, context):
    repo_ext = RepositoryExternal()
    ranking = repo_ext.get_ranking(filter)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(ranking)
    }
