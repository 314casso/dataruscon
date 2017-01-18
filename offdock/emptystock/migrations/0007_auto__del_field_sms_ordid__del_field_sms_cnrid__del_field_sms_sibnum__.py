# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Sms.ordid'
        db.delete_column('emptystock_sms', 'ordid')

        # Deleting field 'Sms.cnrid'
        db.delete_column('emptystock_sms', 'cnrid')

        # Deleting field 'Sms.sibnum'
        db.delete_column('emptystock_sms', 'sibnum')

        # Adding field 'Sms.smsid'
        db.add_column('emptystock_sms', 'smsid',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=50, db_index=True),
                      keep_default=False)

        # Adding field 'Sms.agtid'
        db.add_column('emptystock_sms', 'agtid',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sms.inbox'
        db.add_column('emptystock_sms', 'inbox',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Sms.ordid'
        raise RuntimeError("Cannot reverse this migration. 'Sms.ordid' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Sms.ordid'
        db.add_column('emptystock_sms', 'ordid',
                      self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, db_index=True),
                      keep_default=False)

        # Adding field 'Sms.cnrid'
        db.add_column('emptystock_sms', 'cnrid',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sms.sibnum'
        db.add_column('emptystock_sms', 'sibnum',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Sms.smsid'
        db.delete_column('emptystock_sms', 'smsid')

        # Deleting field 'Sms.agtid'
        db.delete_column('emptystock_sms', 'agtid')

        # Deleting field 'Sms.inbox'
        db.delete_column('emptystock_sms', 'inbox')


    models = {
        'emptystock.contact': {
            'Meta': {'unique_together': "(('contact', 'type'),)", 'object_name': 'Contact'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emptystock.Person']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        'emptystock.person': {
            'Meta': {'object_name': 'Person'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'emptystock.sms': {
            'Meta': {'object_name': 'Sms'},
            'agtid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'http_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbox': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rescount': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'smsid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'xml_response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['emptystock']