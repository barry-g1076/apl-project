
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ALL API API_URL AVAILABLE BOOK BOOKING BOOKINGS BOOKING_ID BY CANCEL CANCELED CONFIRMED DATE EVENTS FETCH FOR FROM ID IN LIST MY NUMBER OF ON PAID PAY PAYMENT_METHOD REGION RESERVATIONS RESERVE SELECT SHOW SORT STATUS STRING TICKET TICKETS TICKET_ID USINGcommand : booking\n| command booking\n| status\n| command status\n| view\n| command view\n| selection\n| command selection\n| sorting\n| command sorting\n| fetching\n| command fetching\n| region\n| command region\n| reservation\n| command reservation\n| listing\n| command listing\n| payment\n| command payment\n| dummydummy : IDbooking : BOOK NUMBER TICKETS FOR STRING ON DATEbooking : BOOK NUMBER TICKETS FOR STRING ON\n| BOOK error TICKETS FOR STRING ON DATE\n| BOOK NUMBER TICKETS FOR STRING ON error\n| BOOK NUMBER TICKETS FOR error ON DATE\n| BOOK error TICKETS FOR error ON DATEstatus : STATUS OF BOOKING BOOKING_ID\n| STATUS OF TICKETSstatus : STATUS OF BOOKING error\n| STATUS OF error\n| STATUS OF\nview : SHOW AVAILABLE TICKETS FOR STRING\n| SHOW MY RESERVATIONS\n| SHOW MY CONFIRMED BOOKINGS\n| SHOW MY PAID TICKETS\n| SHOW MY CANCELED BOOKINGSview : SHOW AVAILABLE TICKETS FOR error\n| SHOW MY error\n| SHOW MY error BOOKINGS\n| SHOW MY error TICKETS\nselection : SELECT TICKET TICKET_IDselection : SELECT TICKET errorsorting : SORT TICKETS BY NUMBER\n| SORT TICKETS BY DATEsorting : SORT TICKETS BY errorfetching : FETCH TICKETS FROM API API_URLfetching : FETCH TICKETS FROM API errorregion : SHOW AVAILABLE TICKETS IN REGIONregion : SHOW AVAILABLE TICKETS errorreservation : RESERVE NUMBER FOR STRING ON DATEreservation : RESERVE error FOR STRING ON DATE\n| RESERVE NUMBER FOR error ON DATE\n| RESERVE NUMBER FOR STRING ON errorlisting : LIST ALL EVENTSlisting : LIST errorpayment : PAY FOR BOOKING BOOKING_ID USING PAYMENT_METHOD\n| CANCEL BOOKING BOOKING_IDpayment : PAY FOR BOOKING error USING PAYMENT_METHOD\n| PAY FOR BOOKING BOOKING_ID USING error\n| CANCEL BOOKING error'
    
_lr_action_items = {'BOOK':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[13,13,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'STATUS':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[14,14,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'SHOW':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[15,15,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'SELECT':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[16,16,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'SORT':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[17,17,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'FETCH':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[18,18,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'RESERVE':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[19,19,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'LIST':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[20,20,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'PAY':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[21,21,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'CANCEL':([0,1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[22,22,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'ID':([0,],[23,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,12,23,24,25,26,27,28,29,30,31,32,33,36,45,51,52,54,58,59,60,65,67,68,71,72,74,76,77,78,79,80,81,82,83,94,95,96,97,98,104,108,109,110,111,112,113,114,115,116,117,118,119,],[0,-1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-21,-22,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-33,-57,-30,-32,-35,-40,-43,-44,-56,-59,-62,-29,-31,-51,-36,-37,-38,-41,-42,-45,-46,-47,-34,-39,-50,-48,-49,-24,-52,-55,-54,-53,-58,-61,-60,-23,-26,-27,-28,-25,]),'NUMBER':([13,19,61,],[34,42,81,]),'error':([13,19,20,36,38,39,47,50,53,61,63,66,69,70,73,84,99,102,104,],[35,43,45,52,58,60,68,72,74,83,86,89,91,92,95,98,109,113,116,]),'OF':([14,],[36,]),'AVAILABLE':([15,],[37,]),'MY':([15,],[38,]),'TICKET':([16,],[39,]),'TICKETS':([17,18,34,35,36,37,56,58,],[40,41,48,49,51,53,77,80,]),'ALL':([20,],[44,]),'FOR':([21,42,43,48,49,53,],[46,63,64,69,70,73,]),'BOOKING':([22,36,46,],[47,50,66,]),'RESERVATIONS':([38,],[54,]),'CONFIRMED':([38,],[55,]),'PAID':([38,],[56,]),'CANCELED':([38,],[57,]),'TICKET_ID':([39,],[59,]),'BY':([40,],[61,]),'FROM':([41,],[62,]),'EVENTS':([44,],[65,]),'BOOKING_ID':([47,50,66,],[67,71,88,]),'IN':([53,],[75,]),'BOOKINGS':([55,57,58,],[76,78,79,]),'DATE':([61,99,100,101,104,105,106,107,],[82,108,110,111,115,117,118,119,]),'API':([62,],[84,]),'STRING':([63,64,69,70,73,],[85,87,90,93,94,]),'REGION':([75,],[96,]),'API_URL':([84,],[97,]),'ON':([85,86,87,90,91,92,93,],[99,100,101,104,105,106,107,]),'USING':([88,89,],[102,103,]),'PAYMENT_METHOD':([102,103,],[112,114,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'command':([0,],[1,]),'booking':([0,1,],[2,24,]),'status':([0,1,],[3,25,]),'view':([0,1,],[4,26,]),'selection':([0,1,],[5,27,]),'sorting':([0,1,],[6,28,]),'fetching':([0,1,],[7,29,]),'region':([0,1,],[8,30,]),'reservation':([0,1,],[9,31,]),'listing':([0,1,],[10,32,]),'payment':([0,1,],[11,33,]),'dummy':([0,],[12,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> command","S'",1,None,None,None),
  ('command -> booking','command',1,'p_command','book_parser.py',15),
  ('command -> command booking','command',2,'p_command','book_parser.py',16),
  ('command -> status','command',1,'p_command','book_parser.py',17),
  ('command -> command status','command',2,'p_command','book_parser.py',18),
  ('command -> view','command',1,'p_command','book_parser.py',19),
  ('command -> command view','command',2,'p_command','book_parser.py',20),
  ('command -> selection','command',1,'p_command','book_parser.py',21),
  ('command -> command selection','command',2,'p_command','book_parser.py',22),
  ('command -> sorting','command',1,'p_command','book_parser.py',23),
  ('command -> command sorting','command',2,'p_command','book_parser.py',24),
  ('command -> fetching','command',1,'p_command','book_parser.py',25),
  ('command -> command fetching','command',2,'p_command','book_parser.py',26),
  ('command -> region','command',1,'p_command','book_parser.py',27),
  ('command -> command region','command',2,'p_command','book_parser.py',28),
  ('command -> reservation','command',1,'p_command','book_parser.py',29),
  ('command -> command reservation','command',2,'p_command','book_parser.py',30),
  ('command -> listing','command',1,'p_command','book_parser.py',31),
  ('command -> command listing','command',2,'p_command','book_parser.py',32),
  ('command -> payment','command',1,'p_command','book_parser.py',33),
  ('command -> command payment','command',2,'p_command','book_parser.py',34),
  ('command -> dummy','command',1,'p_command','book_parser.py',35),
  ('dummy -> ID','dummy',1,'p_dummy','book_parser.py',45),
  ('booking -> BOOK NUMBER TICKETS FOR STRING ON DATE','booking',7,'p_booking','book_parser.py',50),
  ('booking -> BOOK NUMBER TICKETS FOR STRING ON','booking',6,'p_booking_error','book_parser.py',63),
  ('booking -> BOOK error TICKETS FOR STRING ON DATE','booking',7,'p_booking_error','book_parser.py',64),
  ('booking -> BOOK NUMBER TICKETS FOR STRING ON error','booking',7,'p_booking_error','book_parser.py',65),
  ('booking -> BOOK NUMBER TICKETS FOR error ON DATE','booking',7,'p_booking_error','book_parser.py',66),
  ('booking -> BOOK error TICKETS FOR error ON DATE','booking',7,'p_booking_error','book_parser.py',67),
  ('status -> STATUS OF BOOKING BOOKING_ID','status',4,'p_status','book_parser.py',89),
  ('status -> STATUS OF TICKETS','status',3,'p_status','book_parser.py',90),
  ('status -> STATUS OF BOOKING error','status',4,'p_status_error','book_parser.py',98),
  ('status -> STATUS OF error','status',3,'p_status_error','book_parser.py',99),
  ('status -> STATUS OF','status',2,'p_status_error','book_parser.py',100),
  ('view -> SHOW AVAILABLE TICKETS FOR STRING','view',5,'p_view','book_parser.py',119),
  ('view -> SHOW MY RESERVATIONS','view',3,'p_view','book_parser.py',120),
  ('view -> SHOW MY CONFIRMED BOOKINGS','view',4,'p_view','book_parser.py',121),
  ('view -> SHOW MY PAID TICKETS','view',4,'p_view','book_parser.py',122),
  ('view -> SHOW MY CANCELED BOOKINGS','view',4,'p_view','book_parser.py',123),
  ('view -> SHOW AVAILABLE TICKETS FOR error','view',5,'p_view_error','book_parser.py',131),
  ('view -> SHOW MY error','view',3,'p_view_error','book_parser.py',132),
  ('view -> SHOW MY error BOOKINGS','view',4,'p_view_error','book_parser.py',133),
  ('view -> SHOW MY error TICKETS','view',4,'p_view_error','book_parser.py',134),
  ('selection -> SELECT TICKET TICKET_ID','selection',3,'p_selection','book_parser.py',154),
  ('selection -> SELECT TICKET error','selection',3,'p_selection_error','book_parser.py',159),
  ('sorting -> SORT TICKETS BY NUMBER','sorting',4,'p_sorting','book_parser.py',164),
  ('sorting -> SORT TICKETS BY DATE','sorting',4,'p_sorting','book_parser.py',165),
  ('sorting -> SORT TICKETS BY error','sorting',4,'p_sorting_error','book_parser.py',170),
  ('fetching -> FETCH TICKETS FROM API API_URL','fetching',5,'p_fetching','book_parser.py',175),
  ('fetching -> FETCH TICKETS FROM API error','fetching',5,'p_fetching_','book_parser.py',180),
  ('region -> SHOW AVAILABLE TICKETS IN REGION','region',5,'p_region','book_parser.py',184),
  ('region -> SHOW AVAILABLE TICKETS error','region',4,'p_region_error','book_parser.py',189),
  ('reservation -> RESERVE NUMBER FOR STRING ON DATE','reservation',6,'p_reservation','book_parser.py',194),
  ('reservation -> RESERVE error FOR STRING ON DATE','reservation',6,'p_reservation_error','book_parser.py',204),
  ('reservation -> RESERVE NUMBER FOR error ON DATE','reservation',6,'p_reservation_error','book_parser.py',205),
  ('reservation -> RESERVE NUMBER FOR STRING ON error','reservation',6,'p_reservation_error','book_parser.py',206),
  ('listing -> LIST ALL EVENTS','listing',3,'p_listing','book_parser.py',226),
  ('listing -> LIST error','listing',2,'p_listing_error','book_parser.py',231),
  ('payment -> PAY FOR BOOKING BOOKING_ID USING PAYMENT_METHOD','payment',6,'p_payment','book_parser.py',236),
  ('payment -> CANCEL BOOKING BOOKING_ID','payment',3,'p_payment','book_parser.py',237),
  ('payment -> PAY FOR BOOKING error USING PAYMENT_METHOD','payment',6,'p_payment_error','book_parser.py',245),
  ('payment -> PAY FOR BOOKING BOOKING_ID USING error','payment',6,'p_payment_error','book_parser.py',246),
  ('payment -> CANCEL BOOKING error','payment',3,'p_payment_error','book_parser.py',247),
]
