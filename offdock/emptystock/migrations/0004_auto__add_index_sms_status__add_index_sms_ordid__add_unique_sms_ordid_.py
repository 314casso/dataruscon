# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Sms', fields ['status']
        db.create_index('emptystock_sms', ['status'])

        # Adding index on 'Sms', fields ['ordid']
        db.create_index('emptystock_sms', ['ordid'])

        # Adding unique constraint on 'Sms', fields ['ordid']
        db.create_unique('emptystock_sms', ['ordid'])


        # Changing field 'Sms.error_code'
        db.alter_column('emptystock_sms', 'error_code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):
        # Removing unique constraint on 'Sms', fields ['ordid']
        db.delete_unique('emptystock_sms', ['ordid'])

        # Removing index on 'Sms', fields ['ordid']
        db.delete_index('emptystock_sms', ['ordid'])

        # Removing index on 'Sms', fields ['status']
        db.delete_index('emptystock_sms', ['status'])


        # Changing field 'Sms.error_code'
        db.alter_column('emptystock_sms', 'error_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

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
            'cnrid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'rescount': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sibnum': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['emptystock']