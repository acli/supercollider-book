#!/usr/bin/env python
# coding: utf-8

# In[1]:


from music21 import *
from IPython.display import Image as img
from PIL import Image


# (sec-piece-analysis)=
# # Analysis of a Piece
# 
# Let us apply what we have learned by analysing the beginning of the famous piece *Nuvole Bianche* by *Ludovico Enaudi*.
# 
# From the signature of the piece we can see that there are 4 diminished accidentals.
# Using the [circle of fifths](sec-circle-of-fifths) we can deduce that this hints towards either **Ab** (Ab major) or **Fm** (F minor).
# However the piece ends on Ab which strongly hints at **Ab** and indeed that is correct.

# In[2]:


c = converter.parse('./../../../compositions/nuvole_bianche.mxl')
c.metadata.title = 'Nuvole Bianche'
c.metadata.movementName = 'Nuvole Bianche'
c.metadata.composer = 'Ludovico Enaudi'
c.show()


# Therefore, we have the following scale:
# 
# Ab-Bb-C-Db-Eb-F-G-Ab
# 
# with the following chords:
# 
# | Number          | Chord        |
# | --------------- | ------------ |
# | I               | Ab-C-Eb      | 
# | ii              | Bb-Db-F      | 
# | iii             | C-Eb-G       |
# | IV              | Db-F-AB      |
# | V               | Eb-G-Bb      |     
# | vi              | F-Ab-C       |
# | vii             | G-Bb-Db      |
