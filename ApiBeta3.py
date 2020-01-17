import os
import subprocess
import sys
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bitso
from bitso import (AccountRequiredField, AccountStatus, ApiClientError,
                   ApiError, AvailableBooks, Balances, Fees, Funding,
                   FundingDestination, LedgerEntry, Order, OrderBook, Ticker,
                   Trade, TransactionOrder, TransactionQuote, UserTrade,
                   Withdrawal, bitsows)


def OrderBooks():
	try:
		ob = api.order_book('xrp_mxn', aggregate= False)  
		return ob
	except ApiError as error:
		restart(error)

def restart(pError):
    
	#Enviar correo
	# create message object instance
	msg = MIMEMultipart()
	# setup the parameters of the message
	password = "avmm kawq pllp zgju"
	msg['From'] = "pacu280349@gmail.com"
	msg['To'] = "franciscojavierrod2@hotmail.com"
	msg['Subject'] = "Error App"
	# add in the message body
	message = ''

	if pError.args !=None:
		#print('!=none')		
		message = "Ha habido un error en la app:\n Error: %s \n Codigo:%s "%(pError.args[0]['message'],pError.args[0]['code'])
	else:
		message = str(pError)
		#print('else None')
		

	msg.attach(MIMEText(message, 'plain'))
	#create server
	server = smtplib.SMTP('smtp.gmail.com: 587')
	server.starttls()
	# Login Credentials for sending the mail
	server.login(msg['From'], password)
	# send the message via the server.
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	server.quit()
 
	Sub_nam = len(os.path.basename(os.path.abspath(__file__)))
	pathh = str(os.path.abspath(__file__))
 
	lis = ['0202','0201','0203', '0204' ]
	if pError.args ==None:
		print(message)
		script = os.path.join(pathh[:-Sub_nam] , os.path.basename(os.path.abspath(__file__)))
		subprocess.Popen([sys.executable, script, 'restart'])
		sys.exit()
	elif pError.args[0] not in lis:
		print(message)
		script = os.path.join(pathh[:-Sub_nam] , os.path.basename(os.path.abspath(__file__)))
		subprocess.Popen([sys.executable, script, 'restart'])
		sys.exit()
#def restart(pError):--------------------------------------------------------------------------------------------------------------------    
     
     
     

  
def curr_prc():	
	#--- Inicio tick _Muestra el precio actual del XRP
	try:
		tick = api.ticker('xrp_mxn')
		return tick.last
	except ApiError as error:
		restart(error)
	
#***Final tick

#-------------Inicio ventaXRP
def ventaXRP( precio_inicial, fee):
	try:
		precio_venta = precio_inicial / (fee * fee)
		precio_venta = precio_venta - precio_venta % 0.01

		sell = float(precio_venta) * 1.015 # venta con Plus de 1% de ganancia								
		po_price = sell - sell % 0.01
		currentXrpPrc	= float(api.ticker('xrp_mxn'))
		
		mxnDis,xrpDis = BalanceUpdate(priv)

		if float(currentXrpPrc) >= float(po_price):	
			po_price = currentXrpPrc								
			print('Mejor VENDER A: %s que es precio Actual y no a calculado %s '%(str(currentXrpPrc),str(po_price)))								
		else:			 
			print('vender a precio profit %s'%(str(po_price)))
		
		po_major = "%.4f"%xrpDis	
		print('MAJORRRR '+ str(po_major))
		return po_major, po_price
	except ApiError as error:
		restart(error)
	except ApiClientError as error0:
		restart(error0)

	
	
#*************Fin ventaXRP

#---Inicio compraXRP
def compraXRP( precio_inicial, fee):
	try:
		precio_compra = precio_inicial * (fee * fee)

		po_price = float(precio_compra) / 1.015
		po_price = po_price - po_price % 0.01
		print(po_price)
		plus     =  float(mxnDis) / float(po_price)
		po_major = plus - plus % 0.01 #'%.2f'%(float(plus))
		
		print('BUYYYYYYY   '+str(po_price))
		print('XRPPPPPPP   '+str(po_major))
		#time.sleep(1000)
		#return "%.3f"%precio_compra
		return po_major, po_price
	except ApiError as error:
		restart(error)	
#******Final compraXRP

def sortBuyby_f_price(e):
	return e['f_price']

def Ledgar_Trade_Consolidate(pled_operations, plimit, psort, putx_book, ):
	try:	
		#User_Trades
		#utx = priv.user_trades(book ='xrp_mxn', limit=10000, sort='desc',)
		utx = priv.user_trades(book =str(putx_book), 
							   limit=int(plimit), 
							   sort=str(psort))
		#utx-------------------------------------------------

		#Ledger
		ledger = priv.ledger(operations=str(pled_operations),
							 limit=int(plimit), 
							 sort=str(psort))
		#ledger----------------------------------------------
		

		
		ListB = []
		ListS = []
		for le in ledger:
			if le.operation== 'trade' and ( le.operation != 'withdrawal'  or le.operation != 'fundig') :
				for i in utx:
					#de aqui sale un diccionario {'tid': i.tid, 'oper':le.operation, ....}
					if le.balance_updates[0].currency == 'xrp' and i.side == 'buy': # ledger COMPRA	
						Buy={}						
						if le.details['tid'] == i.tid :
							
							Buy['s_tid']      = int(le.details['tid'])							
							Buy['s_tid']      = int(le.details['tid'])
							Buy['s_Ope']      = str(le.operation)
							#print('led Eid:     '+str(le.eid))
							Buy['s_Currency'] = str(le.balance_updates[0].currency)
							Buy['f_CurrAmt']  = str(le.balance_updates[0].amount)							
							Buy['s_oid']       = str(i.oid)
							Buy['s_book']     = str(i.book)	
							#print('UT side    '+str(i.side))
							Buy['s_createdAt'] = str(i.created_at)
							Buy['f_major']     = float(i.major)		
							Buy['f_minor']     = float(i.minor)
							Buy['f_price']     = float(i.price)
							Buy['f_feeCurr']   = str(i.fees_currency)
							Buy['f_feeAmt']    = float(i.fees_amount)
							ListB.append(Buy)
							
					elif le.balance_updates[0].currency == 'mxn' and i.side== 'sell': #ledger VENTA
						Sell = {}
						if le.details['tid'] == i.tid:
							Sell['s_tid']      = le.details['tid']
							Sell['s_Ope']      = le.operation
							#print('led Eid:     '+str(le.eid))
							Sell['s_Currency'] = le.balance_updates[0].currency
							Sell['f_CurrAmt']  = float(le.balance_updates[0].amount)							
							Sell['s_oi']       = i.oid
							Sell['s_book']     = i.book	
							#print('UT side    '+str(i.side))
							Sell['s_createdAt'] = i.created_at
							Sell['f_major']     = i.major		
							Sell['f_minor']     = i.minor
							Sell['f_price']     = i.price
							Sell['f_feeCurr']   = i.fees_currency
							Sell['f_feeAmt']    = i.fees_amount
							ListS.append(Sell)									 					
		return 	ListB, ListS			
	except 	ApiError as error:
		restart(error)
#
"""
b,s = Ledgar_Trade_Consolidate( pled_operations='trades', plimit=1000, psort='desc', putx_book='xrp_mxn')
b.sort(key=sortBuyby_f_price)
for item in b:
	print("Tran Id: %s \nPrice: %s "%(item['s_tid'],item['f_price']))
print('**fin compra***')	
print('')
print('')

s.sort(key=sortBuyby_f_price)
for items in s:
	print( "Tran Id: %s \nPrice: %s "%(items['s_tid'],item['f_price']))
print('***fin venta****')
"""
#def ledger------------------------------------------------------------------------------------------------------------

#Sacar profit comprando con perdida luego re vender 



def wishProfit(lt_price, lt_major, lt_minor, lt_curr, gfee):
	#print(lt_price, lt_major, lt_minor, lt_curr, gfee)
	if lt_curr == 'mxn':		
		plus =  abs(lt_major) * 1.01 
		wp   =  (abs(lt_minor)* gfee )/ plus  
		print('vender para wish Profit '+str(wp))
		res= wp
	else:
		plus = abs(lt_minor) * 1.01
		print(' Plus  '+str(plus))
		wp = abs(plus)/((gfee)*(gfee)*( abs(lt_major)))
		print('wish profit at '+str(wp))
		res = wp
		#print('comprar xrp  '+str(res))
		#print(lt_price, lt_major, lt_minor, lt_curr, gfee)
	#if lt_curr == xrp FIN------------------------------
	return res		
# def wishProfit(**args)-------------------------------------------

def trad():
	try:
		trades = api.trades('xrp_mxn')
		for t in trades:
			print('**************'+str(t))
	except ApiError as error:
		restart(error)	
#def trad():-----------------------------------


#------PlaceOrder()
def PlaceOrder(po_book, po_side, po_order_type, po_major, po_price):
	try:
		order = priv.place_order(book=str(po_book), side=str(po_side), order_type=str(po_order_type), major=str(po_major), price=str(po_price))
		return print('Simula orden(book=str(%s), side=str(%s), order_type=str(%s), major=str(%s), price=str(%s))'%(po_book, po_side, po_order_type, po_major, po_price))

	except ApiError as error:
		restart(error)
	#print('Simula orden(book=str(po_book), side=str(po_side), order_type=str(po_order_type), major=str(po_major), price=str(po_price))')
	#return print('Simula orden(book=str(%s), side=str(%s), order_type=str(%s), major=str(%s), price=str(%s))'%(po_book, po_side, po_order_type, po_major, po_price))	
#def PlaceOrder(po_book, po_side, po_order_type, po_major, po_price):-------------------------------------------------------------------------------------------------

def OpenOrder():
	#--------Open order			
	try:
		oop = priv.open_orders('xrp_mxn')
		return oop
	except ApiError as error:
		#print('Api Error open_orders: \n '+str(error))
		restart(error)
	except ApiClientError as error0:
		restart(error0)
	except Exception as error1:
		restart(error1)	
	#********** fin Open order

#Calcular Porcentaje de perdida, luego poner orden de venta con nuevo precio de venta con recuperacion de perdida
#def user_trades(self, tids=[], book=None, marker=None, limit=25, sort='desc'):
# =----ledger  ( pled_operations='trades', plimit=1000, psort='desc', putx_book='xrp_mxn')
def profitAfterLose(privObj,Book,Sort,iSide=None):		
	pled_operations = 'trades'
	plimit = 150
	if iSide:
		iSide='buy'  		
	else:
		iSide='sell'
	Led = privObj.ledger(operations=str(pled_operations), limit=int(plimit), sort=str(Sort))
	for le in Led:
		print(le.operation)
	pri = privObj.user_trades(book =Book,sort=Sort)
	for i in pri:
		if iSide==i.side:      
			#print(i.tid,i.side,i.major,i.minor,i.price)
   			print(i)		
      
	#time.sleep(100)
#example
# 1. calcular el precio de venta normal.
# 2. calcular el porcentaje de perdida minima.
# 3. Calcular el porcentaje de perdida Maxima.
#
# si la ultima venta fue a un precio de $3.93 MXN 
# me quedo un monto de $95.58 MXN sin comision.
# con Comision calculada, $85.20 libres.
#
# Aplicando Formula de precioProfit 
# 3.93 * (.9935 * .9935 ) , venderia a un precio de $3.8790 MXN
# 
# Calcular el procentaje de Perdida con nuevos precios de Major
#
# porcentaje * NuevoPrecioMarket / ( precioProfit 
# 100 * 4.11 / (3.8790) 
	
	
# def profitAfterLose-------------------------


#global Var
ii     = 0
clock2 = 0
req    = 0
currentPrcLastOrder = '%.2f'%0.01
currentXrpPrc       = '%.2f'%0.01
bal                 = '%.2f'%0.01
oo_id               = ''
ltState             = ''
#----------------------------




def BalanceUpdate(privObj):
	bal = privObj.balances()
	mxnDis = bal.mxn.available
	xrpDis = bal.xrp.available
	print('balance disponible MXN %.2f \n balance disponible XRP %.2f '%(mxnDis, xrpDis))
	return mxnDis,xrpDis

#Iniciar Api Bitso in clock
try:
	#print('Priv')
	priv  = bitso.Api('INCYsSeZSY', '2a729f941e968974ae12c9ec324f2bb2')
	#profitAfterLose(priv,'xrp_mxn','desc',True)
	
except ApiError as error:
	restart(error)
try:
	#print('Api')
	api = bitso.Api()
except ApiError as error:
	restart(error)

try:

	while True:
		
		ii +=1
	
		if ii == 10:
			
			time.sleep(5)
			ii = 0
			#print('**********************************************pausa 5 seg')
		else:
			try:
				mxnDis,xrpDis = BalanceUpdate(priv)
			except ApiError as error:
				restart(error)
			except ApiClientError as error0:
				restart(error0)
			except Exception as error1:
				restart(error1)
			
			
			try:
				oo = OpenOrder()
				req +=1
				if len(oo) > 0:				
					if str(oo_id) != str(oo[0].oid):
						oo_id = oo[0].oid
						print('ORDEN ABIERTA id= '+str(oo))
				else:	
					print('ORDEN no encontrada')				
				req +=1
			except ApiError as error:
				restart(error)
			except ApiClientError as error0:
				restart(error0)
			except Exception as error1:
				restart(error1)		
			#--------- Last User Trade 
			try:
				utx = priv.user_trades(book ='xrp_mxn')
				req += 1
				#UserTrade(tid=13114713, book=xrp_mxn, price=4.08, major=-10.00000000, minor=40.80000000)		
				# checa el precio de la ultima transaccion
			except ApiError as error:
				#print('Api: user_trades:\n'+str(error))
				restart(error)
			except ApiClientError as error0:
				restart(error0)
			except Exception as error1:
				restart(error1)
			#**********fin Last User Trade 
				
				
			#---------- Current Price XRP 
			try:
				xrp = curr_prc()
				if float(currentXrpPrc) != float(xrp): 
					currentXrpPrc = xrp
					print('El precio actual del XRP es:'+str(xrp))	
				req += 1		
			except ApiError as error:
				restart(error)
			#**********fin Current Price XRP

			#---------- Order Book XRP_MXN	
			try:				
				
				ob = api.order_book(book='xrp_mxn', aggregate= False)
				if float(ob.asks[0].price) != float(currentPrcLastOrder):
					#print('%s != %s'%(float(ob.asks[0].price) , float(currentPrcLastOrder)))
					currentPrcLastOrder = ob.asks[0].price		
					print('Venta $%s MXN '%ob.asks[0].price)
					print('Compra $%s MXN '%ob.bids[0].price)
					print('************Lasr ORDER XRP *************'+str(req))
					
				"""				
				#ii = 0
    			if  ii ==0:
					#pError.args[0]['code']
					for i in ob.asks:
						ii += 1
						print('******ORDEN VENTA*******')
						print('Venta \n prc:'+str(i.price) +'\n Amt:'+str(i.amount) )
						
						if ii == 2:
							break
					aa = 0		
					for a in ob.bids:
						aa += 1
						print('******ORDEN COMPRA*******')
						print('compra \n prc:'+str(a.price) +'\n Amt:'+str(a.amount) )									
						
						if aa == 2:
							break
				"""										
				req +=1
			except ApiError as error:				
				restart(error)
			#**********Order Book
			try:
				if len(utx) > 0:
					for i in utx:
						try:
							
							if float(mxnDis) > 10.00 and i.side == 'sell': #si el balance es mayor a 10 mxn entonces compras XRP 
								#print('vamos a comprar xrp con $'+ str(Balances.mxn.available )+' mxn disponibles ')																						
								po_major, po_price = compraXRP(float(i.price), float(.9935))
								s = PlaceOrder('xrp_mxn', 'buy', 'limit', po_major, po_price)
								
								req += 1
							elif float(xrpDis) > 2.00 and i.side == 'buy': # si el balance es mayor a 2 xrp entonces vende XRP
								print('vamos a vender xrp con '+ str(xrpDis )+' XRP disponibles ')
								po_major, po_price = ventaXRP(float(i.price), float(.9935))											
								s = PlaceOrder('xrp_mxn', 'sell', 'limit', po_major, po_price)
								req += 1
							elif float(xrpDis) > 2.00:
								print('Tenemos XRP Disponible: '+str(xrpDis))
							#end if balances.mxn.available > 10.00:---------------------
							#print('Precio de ultima transaccion '+str(i.price) + ' fue una '+ str(i.side))	
						except Exception as error:													
							restart(error)
						if ltState != str(i.tid):
							ltState = str(i.tid)
							print('Last Trade: noid=%s\ncreated_at=%s\nmajor=%s\nminor=%s\nprice=%s\nfee_amt=%s\nfeecurr=%s\nside=%s'%(str(i.oid), str(i.created_at), str(i.major), str(i.minor), str(i.price), str(i.fees_amount), str(i.fees_currency), str(i.side)))
						break						
			except ApiClientError as error:
				restart(error)
			time.sleep(5)			
except ApiError as error:
	restart(error)
