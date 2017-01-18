# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Sms.status'
        db.add_column('emptystock_sms', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Sms.error_code'
        db.add_column('emptystock_sms', 'error_code',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Sms.target'
        db.alter_column('emptystock_sms', 'target', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Sms.sibnum'
        db.alter_column('emptystock_sms', 'sibnum', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Sms.sender'
        db.alter_column('emptystock_sms', 'sender', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):
        # Deleting field 'Sms.status'
        db.delete_column('emptystock_sms', 'status')

        # Deleting field 'Sms.error_code'
        db.delete_column('emptystock_sms', 'error_code')


        # Changing field 'Sms.target'
        db.alter_column('emptystock_sms', 'target', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Sms.sibnum'
        db.alter_column('emptystock_sms', 'sibnum', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Sms.sender'
        db.alter_column('emptystock_sms', 'sender', self.gf('django.db.models.fields.CharField')(max_length=50))

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
            'error_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rescount': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sibnum': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['emptystock']