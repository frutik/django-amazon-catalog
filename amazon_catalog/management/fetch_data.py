from amazonproduct import API
from lxml import etree

from amazon_catalog.models import *

api = API(locale='us')

def _product_lookup(nodeset, section, relationship):
    for node in nodeset:
        i = api.item_lookup(str(node.ASIN))
        try:
            group, created = ProductGroup.objects.get_or_create(name=str(i.Items.Item.ItemAttributes.ProductGroup))
            product, created = Product.objects.get_or_create(
                group=group,
                asin=i.Items.Item.ASIN,
                title=i.Items.Item.ItemAttributes.Title
            )
            product.add_relation(section, relationship)
            AmazonResponse.objects.create(
                product=product,
                raw=etree.tostring(i)
            )
            print i.Items.Item.ItemAttributes.ProductGroup, i.Items.Item.ASIN, i.Items.Item.ItemAttributes.Title
        except Exception, e:
            print '#1', e

def process_most_gifted(category_id, section):
    r = api.browse_node_lookup(category_id, 'MostGifted')
    _product_lookup(r.BrowseNodes.BrowseNode.TopItemSet.TopItem,
                              section,
                              'MostGifted')


def process_top_sellers(category_id, section):
    r = api.browse_node_lookup(category_id, 'TopSellers')
    _product_lookup(r.BrowseNodes.BrowseNode.TopSellers.TopSeller,
                              section,
                              'TopSellers')


def get_products(node_id, path):
    try:
        r = api.browse_node_lookup(node_id, 'BrowseNodeInfo')
        child_nodes = r.BrowseNodes.BrowseNode.Children.BrowseNode
    except AttributeError, e:
        print 'Final node found', node_id
        section, created = CatalogSection.objects.get_or_create(
            path=', '.join(path),
        )
        process_most_gifted(node_id, section)
        process_top_sellers(node_id, section)
    except Exception, e:
        print '#2', e, type(e)
    else:
        for child in child_nodes:
            print child.Name, node_id, child.BrowseNodeId
            section_path = path[:]
            section_path.append(str(child.Name))
            get_products(child.BrowseNodeId, section_path)
    return None

get_products(1000, ['Books'])
