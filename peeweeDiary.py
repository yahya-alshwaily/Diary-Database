from collections import OrderedDict
import datetime
import sys
import os

from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
	content = TextField()
	timestamp = DateTimeField(default=datetime.datetime.now)
	
	class Meta:
		database = db


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
	os.system('cls' if os.name =='nt' else 'clear')


def menu_loop():
	"""Show the menu"""
	choice = None
	
	while choice != 'q':
		clear()
		print('Enter "q" to quit.')
		
		for key, value in menu.items():
			
			print(f'{key}) {value.__doc__}')
		choice = input('Action: ').lower().strip()
		if choice in menu:
			clear()
			menu[choice]()
				
	
def add_entry():
	"""add an entry"""
	print('Enter your entry. Press ctrl+d when finished.')
	data = sys.stdin.read().strip()
	
	if data:
		if input('Save entry? [Y/N] ').lower() != 'n':
			
			Entry.create(content=data)
			print('Saved successfully!')


def view_entry(search_query = None):
	"""View previous entries"""
	
	entries = Entry.select().order_by(Entry.timestamp.desc())

	if search_query:
		
		entries = entries.where(Entry.content.contains(search_query))
	
	for entry in entries:
		timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M %p')
		clear()
		print(timestamp)
		print('='*len(timestamp))
		print(entry.content)
		print('\n\n'+ '='*len(timestamp))
		print('N) for next entry')
		print('D) delete the entry')
		print('q) return for main menu')
		
		next_action = input('Action[N/Q/D]: ').lower().strip()
		if next_action == 'q':
			break
		elif next_action =='d':
			delete_entry(entry)


def search_entry():
	"""Searches for a entry"""
	search_query = input("what would you like to search for? ")
	view_entry(search_query)

			
def delete_entry(entry):
	"""delete an entry"""
	if input('Are you sure? [Y/N]: ').lower() == 'y':
		entry.delete_instance()
		print('Entry deleted')
		
menu = OrderedDict([
	('a', add_entry),
	('v', view_entry),
	('s', search_entry),
	])
					
if __name__=='__main__':
	initialize()
	menu_loop()