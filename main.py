from analyzer.PostAnalyzer import PostAnalyzer
import FacadeAnalyzePost
from entity.CrawledData import CrawledData
from entity.Restaurant import Restaurant
from entity.Filter import Filter

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
