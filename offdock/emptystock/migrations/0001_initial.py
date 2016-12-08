# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('emptystock_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('emptystock', ['Person'])

        # Adding model 'Contact'
        db.create_table('emptystock_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emptystock.Person'])),
        ))
        db.send_create_signal('emptystock', ['Contact'])

        # Adding unique constraint on 'Contact', fields ['contact', 'type']
        db.create_unique('emptystock_contact', ['contact', 'type'])


    def backwards(self, orm):
        # Removing unique constraint on 'Contact', fields ['contact', 'type']
        db.delete_unique('emptystock_contact', ['contact', 'type'])

        # Deleting model 'Person'
        db.delete_table('emptystock_person')

        # Deleting model 'Contact'
        db.delete_table('emptystock_contact')


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
        }
    }

    complete_apps = ['emptystock']