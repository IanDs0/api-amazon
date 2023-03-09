from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException

from dotenv import load_dotenv

import datetime
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define as credenciais de acesso da AWS
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
partner_tag = os.getenv('PARTNER_TAG')
host = os.getenv('HOST')
region = os.getenv('REGION')


def json(retorno):
    price = float(retorno.offers.listings[0].price.display_amount.replace('R$', '').strip().replace('.', '').replace(',', '.'))
    return {
        "product_store_id": str(retorno.asin),
        "product_url": str(retorno.detail_page_url),
        "product_name": str(retorno.item_info.title.display_value),
        "product_price": float(price),
        "product_loja": str("Amazon"),
        "product_image_url": str(retorno.images.primary.medium.url),
        "product_category": str("category"),
    }


def Search(Keywords, SearchIndex, ItemCount):
    # Cria uma instância do objeto DefaultApi
    api_instance = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    keywords = Keywords
    search_index = SearchIndex
    item_count = 2
    search_items_resource = [
        SearchItemsResource.ITEMINFO_CLASSIFICATIONS,
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.IMAGES_PRIMARY_MEDIUM,
        SearchItemsResource.OFFERS_LISTINGS_PRICE,
    ]

    # Define os parâmetros de pesquisa
    try:
        search_request = SearchItemsRequest(
            partner_tag=partner_tag,
            partner_type=PartnerType.ASSOCIATES,
            keywords=keywords,
            search_index=search_index,
            item_count=item_count,
            resources=search_items_resource,
        )
    except ValueError as exception:
        print("Error in forming SearchItemsRequest: ", exception)
        return "Error"

    try:
        """ Sending request """
        response = (api_instance.search_items(search_request))

        print("API called Successfully")
        # print("Comple te Response:", response)

        """ Parse response """
        if response.search_result is not None:
            print("Printing first item information in SearchResult:")
            array_item = []
            for item in response.search_result.items:
                # print(item)
                if item is not None:
                    if item.detail_page_url is not None:
                        if (
                                item.item_info is not None
                                and item.item_info.title is not None
                                and item.item_info.title.display_value is not None
                        ):
                            if (
                                    item.offers is not None
                                    and item.offers.listings is not None
                                    and item.offers.listings[0].price is not None
                                    and item.offers.listings[0].price.display_amount is not None
                            ):
                                if (
                                        item.images is not None
                                        and item.images.primary is not None
                                        and item.images.primary.medium is not None
                                        and item.images.primary.medium.url is not None
                                ):
                                    # if (
                                    #     item.item_info is not None
                                    #     and item.item_info.classifications is not None
                                    #     and item.item_info.classifications.binding is not None
                                    #     and item.item_info.classifications.binding.display_value is not None
                                    # ):
                                        array_item.append(json(item))

            response.search_result = {
                "Products": array_item
            }
            return response

        if response.errors is not None:
            print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
            print("Error code", response.errors[0].code)
            print("Error message", response.errors[0].message)
            return response.errors[0]

    except ApiException as exception:
        print("Error calling PA-API 5.0!")
        print("Status code:", exception.status)
        print("Errors :", exception.body)
        print("Request ID:", exception.headers["x-amzn-RequestId"])

    except TypeError as exception:
        print("TypeError :", exception)

    except ValueError as exception:
        print("ValueError :", exception)

    except Exception as exception:
        print("Exception :", exception)
