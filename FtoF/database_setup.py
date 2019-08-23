
from sqlalchemy import Integer, String, Column, ForeignKey
import os, sys
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base= declarative_base()


class Voulent(Base):
	""" docdtring for Voulenter """
	__tablename__ = 'voulent'
	id = Column(Integer, primary_key =True)
	name = Column( String(30), nullable = False)
	email = Column(String(30), nullable = False)
	phone = Column(Integer, nullable = False, unique = True)
	password = Column(String(20), nullable = False)
	pincode = Column(Integer, nullable = False)
	aadhaar = Column(Integer, nullable = False, unique = True)
	address = Column(String(250), nullable = False)
	# voulenter_pic = Column(String(250), nullable = False)
	

class Crop(Base):
	__tablename__ = 'crop'
	id = Column(Integer, primary_key = True)
	name = Column(String(50), nullable = False)
	catagory_id = Column(Integer, nullable = False)
	catagory_name = Column(String(50), nullable = False)
	# crop_id = relationship('Farmer', backref = 'crop.id')
	# cat_id = relationship('Farmer', backref = 'crop.catagory_id')


class Farmer(Base):
	"""docstring for User"""
	__tablename__ = 'farmer'
	id = Column(Integer, primary_key = True)
	name = Column(String(30), nullable = False)
	pincode = Column(Integer, nullable = False)
	phone = Column(Integer, nullable = False, unique = True)
	address = Column(String(300), nullable = False, unique = True)
	voulenter_id = Column(Integer, ForeignKey('voulent.id'))
	catagory_id = Column(Integer, nullable = False)
	# catagory_id = Column(Integer,ForeignKey('crop.catagory_id'))	
	catagory_name = Column(String(50), nullable = False)
	# crop_id = Column(Integer, ForeignKey('crop.id'))
	crop_id = Column(Integer, nullable = False)
	crop_name = Column(String(50), nullable = False)
	quantity = Column(Integer, nullable =False)
	voulent = relationship(Voulent)



class Customer(Base):
	__tablename__ = 'customer'
	id = Column(Integer, primary_key = True)
	name= Column(String(30), nullable = False)
	pincode = Column(Integer, nullable = False)
	phone = Column(Integer, nullable = False, unique = True)
	email = Column(String(30), nullable = False)
	password = Column(String(20), nullable = False)
	aadhaar = Column(Integer, nullable = False, unique = True)
	address = Column(String(300), nullable = False)
	vol_phone = Column(Integer, nullable = False)
	voulenter_id = Column(Integer, ForeignKey('voulent.id'))
	customer_pic = Column(String(250), nullable = False)
	voulent = relationship(Voulent)

class Kart(Base):
	__tablename__ = 'kart'
	id = Column(Integer, primary_key = True )
	quantity = Column(Integer, nullable = False)
	crop_id = Column(Integer, ForeignKey('crop.id'))
	customer_id = Column(Integer, ForeignKey('customer.id'))
	farmer_id = Column(Integer, ForeignKey('farmer.id'))
	voulenter_id = Column(Integer, ForeignKey('voulent.id'))
	crop = relationship(Crop)
	customer = relationship(Customer)
	farmer = relationship(Farmer)
	voulent = relationship(Voulent)


engine = create_engine('sqlite:///farmerdatabase.db')
Base.metadata.create_all(engine)
