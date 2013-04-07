from amazonproduct import API
# from lxml import etree

from django.core.management.base import BaseCommand

from amazon_catalog.models import *
api = API(locale='us')
class Command(BaseCommand):
    can_import_settings = True
    args = 'category_id category_name'
    help = 'Import products from given category'

    def handle(self, *args, **kwargs):
        if args:
            args = list(args)
            id = args.pop(0)
            name = args.pop(0)
            get_products(id, [name])
        else:
            print "See python manage.py help fetch_data for correct usage example"

def _product_lookup(nodeset, section, relationship):
    ids = [str(node.ASIN) for node in nodeset]
    try:
        r = api.item_lookup(','.join(ids))
    except Exception, e:
        print '#11', e
        return None

    for i in r.Items.Item:
        try:
            group, created = ProductGroup.objects.get_or_create(
                name=str(i.ItemAttributes.ProductGroup)
            )

            product, created = Product.objects.get_or_create(
                group=group,
                asin=i.ASIN,
                title=i.ItemAttributes.Title
            )

            product.add_relation(section, relationship)

            print i.ItemAttributes.ProductGroup, i.ASIN, i.ItemAttributes.Title

        except Exception, e:
            print '#1', e

def process_most_gifted(category_id, section):
    r = api.browse_node_lookup(category_id, 'MostGifted')
    _product_lookup(r.BrowseNodes.BrowseNode.TopItemSet.TopItem,
                              section,
                              'MostGifted')

def process_most_wished(category_id, section):
    r = api.browse_node_lookup(category_id, 'MostWishedFor')
    _product_lookup(r.BrowseNodes.BrowseNode.TopItemSet.TopItem,
                              section,
                              'MostWishedFor')

def process_new_releases(category_id, section):
    r = api.browse_node_lookup(category_id, 'NewReleases')
    _product_lookup(r.BrowseNodes.BrowseNode.TopItemSet.TopItem,
                              section,
                              'NewReleases')

def process_top_sellers(category_id, section):
    r = api.browse_node_lookup(category_id, 'TopSellers')
    _product_lookup(r.BrowseNodes.BrowseNode.TopSellers.TopSeller,
                              section,
                              'TopSellers')

PROCESSINGS_TYPES = (
    process_most_gifted,
    process_top_sellers,
    process_most_wished,
    process_new_releases
)

def get_products(node_id, path):
    try:
        r = api.browse_node_lookup(node_id, 'BrowseNodeInfo')
        child_nodes = r.BrowseNodes.BrowseNode.Children.BrowseNode

    except AttributeError, e:
        print 'Final node found', node_id

        section, created = CatalogSection.objects.get_or_create(
            path=', '.join(path),
        )
        for t in PROCESSINGS_TYPES:
            try:
                t(node_id, section)
            except Exception, e:
                print e

    except Exception, e:
        print '#2', e, type(e)

    else:
        for child in child_nodes:
            print child.Name, node_id, child.BrowseNodeId
            section_path = path[:]
            section_path.append(str(child.Name))
            get_products(child.BrowseNodeId, section_path)

    return None
#
# get_products(1000, ['Books'])
