# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductGroup'
        db.create_table('amazon_catalog_productgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('amazon_catalog', ['ProductGroup'])

        # Adding model 'ProductSectionRelationship'
        db.create_table('amazon_catalog_productsectionrelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['amazon_catalog.Product'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['amazon_catalog.CatalogSection'])),
            ('relation_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('amazon_catalog', ['ProductSectionRelationship'])

        # Adding model 'Product'
        db.create_table('amazon_catalog_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asin', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['amazon_catalog.ProductGroup'])),
        ))
        db.send_create_signal('amazon_catalog', ['Product'])

        # Adding model 'CatalogSection'
        db.create_table('amazon_catalog_catalogsection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.TextField')(unique=True)),
        ))
        db.send_create_signal('amazon_catalog', ['CatalogSection'])

        # Adding model 'AmazonResponse'
        db.create_table('amazon_catalog_amazonresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='amazon_responses', to=orm['amazon_catalog.Product'])),
            ('raw', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('amazon_catalog', ['AmazonResponse'])


    def backwards(self, orm):
        # Deleting model 'ProductGroup'
        db.delete_table('amazon_catalog_productgroup')

        # Deleting model 'ProductSectionRelationship'
        db.delete_table('amazon_catalog_productsectionrelationship')

        # Deleting model 'Product'
        db.delete_table('amazon_catalog_product')

        # Deleting model 'CatalogSection'
        db.delete_table('amazon_catalog_catalogsection')

        # Deleting model 'AmazonResponse'
        db.delete_table('amazon_catalog_amazonresponse')


    models = {
        'amazon_catalog.amazonresponse': {
            'Meta': {'object_name': 'AmazonResponse'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'amazon_responses'", 'to': "orm['amazon_catalog.Product']"}),
            'raw': ('django.db.models.fields.TextField', [], {})
        },
        'amazon_catalog.catalogsection': {
            'Meta': {'object_name': 'CatalogSection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'product': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'sections'", 'null': 'True', 'through': "orm['amazon_catalog.ProductSectionRelationship']", 'to': "orm['amazon_catalog.Product']"})
        },
        'amazon_catalog.product': {
            'Meta': {'object_name': 'Product'},
            'asin': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['amazon_catalog.ProductGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'amazon_catalog.productgroup': {
            'Meta': {'object_name': 'ProductGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'amazon_catalog.productsectionrelationship': {
            'Meta': {'object_name': 'ProductSectionRelationship'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['amazon_catalog.Product']"}),
            'relation_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['amazon_catalog.CatalogSection']"})
        }
    }

    complete_apps = ['amazon_catalog']