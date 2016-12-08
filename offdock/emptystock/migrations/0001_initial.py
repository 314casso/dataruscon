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
        ))
        db.send_create_signal('emptystock', ['Person'])

        # Adding M2M table for field contacts on 'Person'
        m2m_table_name = db.shorten_name('emptystock_person_contacts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['emptystock.person'], null=False)),
            ('contact', models.ForeignKey(orm['emptystock.contact'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'contact_id'])

        # Adding model 'Contact'
        db.create_table('emptystock_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=2)),
        ))
        db.send_create_signal('emptystock', ['Contact'])

        # Adding unique constraint on 'Contact', fields ['contact', 'type']
        db.create_unique('emptystock_contact', ['contact', 'type'])


    def backwards(self, orm):
        # Removing unique constraint on 'Contact', fields ['contact', 'type']
        db.delete_unique('emptystock_contact', ['contact', 'type'])

        # Deleting model 'Person'
        db.delete_table('emptystock_person')

        # Removing M2M table for field contacts on 'Person'
        db.delete_table(db.shorten_name('emptystock_person_contacts'))

        # Deleting model 'Contact'
        db.delete_table('emptystock_contact')


    models = {
        'emptystock.contact': {
            'Meta': {'unique_together': "(('contact', 'type'),)", 'object_name': 'Contact'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        'emptystock.person': {
            'Meta': {'object_name': 'Person'},
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['emptystock.Contact']", 'symmetrical': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['emptystock']