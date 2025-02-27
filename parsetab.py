
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'API API_URL AVAILABLE BOOK BOOKING BOOKING_ID BY CANCEL DATE DETAILS EVENT EVENTS FETCH FOR FROM IN LIST MY NUMBER ON OUT PAY PAYMENT_METHOD PRICE READ REGION RESERVE SELECT SHOW SORT STATUS TICKETS TICKET_ID USINGstatement : book_statement\n| status_statement\n| show_statement\n| select_statement\n| sort_statement\n| fetch_statement\n| reserve_statement\n| region_statement\n| speech_statement\n| list_statement\n| pay_statement\n| cancel_statementbook_statement : BOOK NUMBER TICKETS FOR EVENT ON DATEstatus_statement : STATUS BOOKING_IDshow_statement : SHOW AVAILABLE TICKETSselect_statement : SELECT TICKET_IDsort_statement : SORT TICKETS BY PRICEfetch_statement : FETCH TICKETS FROM API API_URLreserve_statement : RESERVE TICKETS FOR EVENTregion_statement : SHOW AVAILABLE TICKETS IN REGIONspeech_statement : READ OUT MY BOOKING DETAILS\n| READ AVAILABLE TICKETS FOR EVENTlist_statement : LIST EVENTSpay_statement : PAY BOOKING_ID USING PAYMENT_METHODcancel_statement : CANCEL BOOKING_ID'
    
_lr_action_items = {'BOOK':([0,],[14,]),'STATUS':([0,],[15,]),'SHOW':([0,],[16,]),'SELECT':([0,],[17,]),'SORT':([0,],[18,]),'FETCH':([0,],[19,]),'RESERVE':([0,],[20,]),'READ':([0,],[21,]),'LIST':([0,],[22,]),'PAY':([0,],[23,]),'CANCEL':([0,],[24,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,12,13,26,28,34,36,38,47,49,52,54,55,56,57,59,],[0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-14,-16,-23,-25,-15,-17,-19,-24,-20,-18,-21,-22,-13,]),'NUMBER':([14,],[25,]),'BOOKING_ID':([15,23,24,],[26,35,36,]),'AVAILABLE':([16,21,],[27,33,]),'TICKET_ID':([17,],[28,]),'TICKETS':([18,19,20,25,27,33,],[29,30,31,37,38,43,]),'OUT':([21,],[32,]),'EVENTS':([22,],[34,]),'BY':([29,],[39,]),'FROM':([30,],[40,]),'FOR':([31,37,43,],[41,45,51,]),'MY':([32,],[42,]),'USING':([35,],[44,]),'IN':([38,],[46,]),'PRICE':([39,],[47,]),'API':([40,],[48,]),'EVENT':([41,45,51,],[49,53,57,]),'BOOKING':([42,],[50,]),'PAYMENT_METHOD':([44,],[52,]),'REGION':([46,],[54,]),'API_URL':([48,],[55,]),'DETAILS':([50,],[56,]),'ON':([53,],[58,]),'DATE':([58,],[59,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'book_statement':([0,],[2,]),'status_statement':([0,],[3,]),'show_statement':([0,],[4,]),'select_statement':([0,],[5,]),'sort_statement':([0,],[6,]),'fetch_statement':([0,],[7,]),'reserve_statement':([0,],[8,]),'region_statement':([0,],[9,]),'speech_statement':([0,],[10,]),'list_statement':([0,],[11,]),'pay_statement':([0,],[12,]),'cancel_statement':([0,],[13,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> book_statement','statement',1,'p_statement','book_parser.py',9),
  ('statement -> status_statement','statement',1,'p_statement','book_parser.py',10),
  ('statement -> show_statement','statement',1,'p_statement','book_parser.py',11),
  ('statement -> select_statement','statement',1,'p_statement','book_parser.py',12),
  ('statement -> sort_statement','statement',1,'p_statement','book_parser.py',13),
  ('statement -> fetch_statement','statement',1,'p_statement','book_parser.py',14),
  ('statement -> reserve_statement','statement',1,'p_statement','book_parser.py',15),
  ('statement -> region_statement','statement',1,'p_statement','book_parser.py',16),
  ('statement -> speech_statement','statement',1,'p_statement','book_parser.py',17),
  ('statement -> list_statement','statement',1,'p_statement','book_parser.py',18),
  ('statement -> pay_statement','statement',1,'p_statement','book_parser.py',19),
  ('statement -> cancel_statement','statement',1,'p_statement','book_parser.py',20),
  ('book_statement -> BOOK NUMBER TICKETS FOR EVENT ON DATE','book_statement',7,'p_book_statement','book_parser.py',26),
  ('status_statement -> STATUS BOOKING_ID','status_statement',2,'p_status_statement','book_parser.py',32),
  ('show_statement -> SHOW AVAILABLE TICKETS','show_statement',3,'p_show_statement','book_parser.py',38),
  ('select_statement -> SELECT TICKET_ID','select_statement',2,'p_select_statement','book_parser.py',44),
  ('sort_statement -> SORT TICKETS BY PRICE','sort_statement',4,'p_sort_statement','book_parser.py',50),
  ('fetch_statement -> FETCH TICKETS FROM API API_URL','fetch_statement',5,'p_fetch_statement','book_parser.py',56),
  ('reserve_statement -> RESERVE TICKETS FOR EVENT','reserve_statement',4,'p_reserve_statement','book_parser.py',62),
  ('region_statement -> SHOW AVAILABLE TICKETS IN REGION','region_statement',5,'p_region_statement','book_parser.py',67),
  ('speech_statement -> READ OUT MY BOOKING DETAILS','speech_statement',5,'p_speech_statement','book_parser.py',72),
  ('speech_statement -> READ AVAILABLE TICKETS FOR EVENT','speech_statement',5,'p_speech_statement','book_parser.py',73),
  ('list_statement -> LIST EVENTS','list_statement',2,'p_list_statement','book_parser.py',82),
  ('pay_statement -> PAY BOOKING_ID USING PAYMENT_METHOD','pay_statement',4,'p_pay_statement','book_parser.py',88),
  ('cancel_statement -> CANCEL BOOKING_ID','cancel_statement',2,'p_cancel_statement','book_parser.py',94),
]
