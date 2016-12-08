# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field contacts on 'Person'
        db.delete_table(db.shorten_name('emptystock_person_contacts'))

        # Adding field 'Contact.person'
        db.add_column('emptystock_contact', 'person',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=7, to=orm['emptystock.Person']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding M2M table for field contacts on 'Person'
        m2m_table_name = db.shorten_name('emptystock_person_contacts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['emptystock.person'], null=False)),
            ('contact', models.ForeignKey(orm['emptystock.contact'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'contact_id'])

        # Deleting field 'Contact.person'
        db.delete_column('emptystock_contact', 'person_id')


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
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['emptystock']