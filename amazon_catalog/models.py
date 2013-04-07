from django.db import models

class ProductGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class ProductSectionRelationship(models.Model):
    product = models.ForeignKey('Product', db_index=True)
    section = models.ForeignKey('CatalogSection', db_index=True)
    relation_type = models.CharField(max_length=255)

class Product(models.Model):
    asin = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    group = models.ForeignKey(ProductGroup)

    def __unicode__(self):
        return self.title

    def add_relation(self, section, relation_type):
        return ProductSectionRelationship.objects.get_or_create(
            product=self,
            section=section,
            relation_type=relation_type)

class CatalogSection(models.Model):
    path = models.TextField(unique=True)
    product = models.ManyToManyField(Product, null=True, related_name='sections', through='ProductSectionRelationship')

    def __unicode__(self):
        return self.path

class AmazonResponse(models.Model):
    product = models.ForeignKey(Product, related_name='amazon_responses')
    raw = models.TextField()

    def __unicode__(self):
        return self.title
