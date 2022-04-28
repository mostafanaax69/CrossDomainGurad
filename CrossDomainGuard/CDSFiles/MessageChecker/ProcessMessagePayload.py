import CrossDomainGuard.MessageChecker.dataStructures as ds
import CrossDomainGuard.MessageChecker.CreditCardCheckerAlgoirthm as checkcredit
import CrossDomainGuard.MessageChecker.MessageBuilder as msgRespBuilder

paymentOpBodyFields = ['country_id', 'currency_id', 'amount', 'info', 'Payment_Reciever', 'Transaction_Date']
paymentOpIndoBodyFields = ['issuer', 'CreditCardNumber', 'consumer_name', 'ccv', 'consumer_bank', 'bank_code',
                           'account_number']
detailsOpBodyFields = ['Transaction_ID', 'Payment_Reciever']
refundOpBodyFields = ['Transaction_ID', 'amount', 'Payment_Reciever']

responseDetailsPayloadBody = ['Transaction Details', 'success', 'message']
responeDetailsPayloadInnerbody = ['country_id', 'currency_id', 'amount', 'info', 'Payment_Reciever', 'Transaction_Date',
                                  'Transaction_ID']
responsePaymentPayloadBody = ['Transaction Payment', 'success', 'message']
responeRefundPayloadBody = ['Transaction Refund', 'success', 'message']
responseCancelPayloadBody = ['Transaction Cancel', 'success', 'message']

MessageVals = ['OK', 'Transaction not found', 'not allowed amount', 'WRONG PARAMTERS', 'WRONG VALUES']
MessageSuc = ['True', 'False']

dictionary_requestParams_response_error = {
    'Transaction':
        {
            "Transaction_ID": "not important",
        },
    'success': "false",
    'message': "WRONG PARAMTERS",
}

dictionary_request_response_value_error = {
    'Transaction':
        {
            "Transaction_ID": "not important",
        },
    'success': "false",
    'message': "WRONG VALUES",
}

msg_host = 'cdg.creditcard.com'
curr_year = '22'
curr_month = '4'


def are_eq(a, b):
    return set(a).__eq__(set(b)) and len(a) == len(b)


def checkBank(bank, bankcode):
    if bank not in ds.supportedBanks.keys(): return False
    if not bankcode == ds.bankCode[bank]: return False
    return True


def checkAccountNumber(accountnum, bank, creditcardnum, country):
    if len(accountnum) != 9: return False
    creditcardlast2digits = creditcardnum[-2:]
    legitAccNum = country + creditcardlast2digits + ds.supportedBanks[bank] + ds.bankCode[bank]
    if legitAccNum != accountnum: return False
    return True


def checkTransactionFormat(Trans_ID):
    if Trans_ID[0] != 'T': return False
    if Trans_ID[1] + Trans_ID[2] != curr_year: return False
    if Trans_ID[3] != curr_month: return False
    if (len(Trans_ID[4:])) != 8: return False
    if Trans_ID not in ds.TransactionNumbers.keys(): return False

    return True


class PayloadProcessing:
    def __init__(self):
        pass

    def processPayload(self, payloadDic, op, src, MsgID):
        ############## processing message request PAYLOAD
        if src == 'Client':
            ################# processing payment operation PAYLOAD
            if op == 'transaction':
                ################################# checking body headers amount and keys
                if not are_eq(payloadDic['Transaction'].keys(), paymentOpBodyFields):
                    resp = msgRespBuilder.ServerResponse().Create_Payment_Response_fail(
                        dictionary_requestParams_response_error, msg_host, MsgID)
                    return resp, False
                if not are_eq(payloadDic['Transaction']['info'].keys(), paymentOpIndoBodyFields):
                    resp = msgRespBuilder.ServerResponse().Create_Payment_Response_fail(
                        dictionary_requestParams_response_error, msg_host, MsgID)
                    return resp, False
                ###################### PAYMENT BODY VALUES VALIDATION
                if not self.valdiatePaymentOperationFields(payloadDic):
                    resp = msgRespBuilder.ServerResponse().Create_Payment_Response_fail(
                        dictionary_request_response_value_error, msg_host, MsgID)
                    return resp, False

            if op == 'details':
                if not are_eq(payloadDic['Transaction'].keys(), detailsOpBodyFields):
                    resp = msgRespBuilder.ServerResponse().Create_Details_response_fail(
                        dictionary_requestParams_response_error, msg_host, MsgID)
                    return resp, False
                ########## VALIDATE FIELDS CONTENT values
                if not self.validateDetailsOperationFields(payloadDic):
                    resp = msgRespBuilder.ServerResponse().Create_Details_response_fail(
                        dictionary_request_response_value_error, msg_host, MsgID)
                    return resp, False

            if op == 'refund':
                if not are_eq(payloadDic['Transaction'].keys(), refundOpBodyFields):

                    resp = msgRespBuilder.ServerResponse().Create_Refund_response_fail(
                        dictionary_requestParams_response_error, msg_host, MsgID)
                    return resp, False
                ########## VALIDATE FIELDS CONTENT values
                if not self.validateRefundOperationFields(payloadDic):
                    resp = msgRespBuilder.ServerResponse().Create_Refund_response_fail(
                        dictionary_request_response_value_error, msg_host, MsgID)
                    return resp, False

            if op == 'cancel':
                if not are_eq(payloadDic['Transaction'].keys(), detailsOpBodyFields):
                    resp = msgRespBuilder.ServerResponse().Create_cancel_response_fail(
                        dictionary_requestParams_response_error, msg_host, MsgID)
                    return resp, False
                ########## VALIDATE FIELDS CONTENT values
                if not self.validateDetailsOperationFields(payloadDic):
                    resp = msgRespBuilder.ServerResponse().Create_cancel_response_fail(
                        dictionary_request_response_value_error, msg_host, MsgID)
                    return resp, False

            return 'PayLoad OK', True

        if src == 'Server':
            OperationType = list(payloadDic.keys())[0].split(" ")
            if OperationType[1] == 'Details':
                if not are_eq(payloadDic.keys(), responseDetailsPayloadBody):
                    return 'Drop', False

                if not are_eq(payloadDic['Transaction Details'].keys(), responeDetailsPayloadInnerbody):
                    return 'Drop', False

                if not are_eq(payloadDic['Transaction Details']['info'].keys(), paymentOpIndoBodyFields):
                    return 'Drop', False

                if not self.valdiateDetailstOperationResponeFields(payloadDic):
                    return 'Drop', False

                if payloadDic['success'] not in MessageSuc:
                    return 'Drop', False

                if payloadDic['message'] not in MessageVals:
                    return 'Drop', False

            if OperationType[1] == 'Payment':

                if not are_eq(payloadDic.keys(), responsePaymentPayloadBody):
                    return 'Drop', False
                if not checkTransactionFormat(payloadDic['Transaction Payment']['Transaction_ID']):
                    return 'Drop', False

                if payloadDic['success'] not in MessageSuc:
                    return 'Drop', False

                if payloadDic['message'] not in MessageVals:
                    return 'Drop', False

            if OperationType[1] == 'Refund':
                if not are_eq(payloadDic.keys(), responeRefundPayloadBody):
                    return 'Drop', False

                if not checkTransactionFormat(payloadDic['Transaction Refund']['Transaction_ID']):
                    return 'Drop', False

                if int(payloadDic['Transaction Refund']['amount']) < 0:
                    return 'Drop', False

                if ds.TransactionsAmounts[payloadDic['Transaction Refund']['Transaction_ID']] < int(
                        payloadDic['Transaction Payment']['amount']):
                    return 'Drop', False

                if payloadDic['success'] not in MessageSuc:
                    return 'Drop', False

                if payloadDic['message'] not in MessageVals:
                    return 'Drop', False

            if OperationType[1] == 'Cancel':
                if not are_eq(payloadDic.keys(), responseCancelPayloadBody):
                    return 'Drop', False
                if not checkTransactionFormat(payloadDic['Transaction Cancel']['Transaction_ID']):
                    return 'Drop', False

                if payloadDic['success'] not in MessageSuc:
                    return 'Drop', False

                if payloadDic['message'] not in MessageVals:
                    return 'Drop', False

            return 'PayLoad OK', True

    def valdiateDetailstOperationResponeFields(self, payloadDic):
        dic = payloadDic['Transaction Details']
        info_dic = dic['info']
        flag = True
        transAllowedAmount = ds.maxAmountdict[
            info_dic['consumer_name'] + '-' + dic['Payment_Reciever']]
        if len(dic['country_id']) != 2 or dic[
            'country_id'] not in ds.supportedCountries: flag = False
        if len(dic['currency_id']) != 3 or dic[
            'currency_id'] not in ds.supportedCurrines: flag = False
        if info_dic['consumer_name'] + '-' + dic[
            'Payment_Reciever'] not in ds.maxAmountdict: flag = False
        if int(dic['amount']) < 0: flag = False
        if int(dic['amount']) > int(transAllowedAmount): flag = False
        if not checkcredit.check_valid_card(card_number=info_dic['CreditCardNumber'],
                                            card_cvv=info_dic['ccv']): flag = False
        if not checkBank(info_dic['consumer_bank'], info_dic['bank_code']): flag = False
        if not checkAccountNumber(info_dic['account_number'], info_dic['consumer_bank'],
                                  info_dic['CreditCardNumber'],
                                  dic['country_id']): flag = False

        if not checkTransactionFormat(dic['Transaction_ID']): flag = False
        if ds.TransactionNumbers[dic['Transaction_ID']] != dic['Payment_Reciever']: flag = False

        return flag

    def validateRefundOperationFields(self, payloadDic):
        dic = payloadDic['Transaction']
        flag = True
        if len(dic['Transaction_ID']) != 12: flag = False
        if not checkTransactionFormat(dic['Transaction_ID']): flag = False
        if ds.TransactionNumbers[dic['Transaction_ID']] != dic['Payment_Reciever']: flag = False
        if int(dic['amount']) < 0: flag = False
        if int(dic['amount']) > ds.TransactionsAmounts[dic['Transaction_ID']]: flag = False

        return flag

    def validateDetailsOperationFields(self, payloadDic):
        dic = payloadDic['Transaction']
        flag = True
        if len(dic['Transaction_ID']) != 12: flag = False
        if not checkTransactionFormat(dic['Transaction_ID']): flag = False
        if ds.TransactionNumbers[dic['Transaction_ID']] != dic['Payment_Reciever']: flag = False

        return flag

    def valdiatePaymentOperationFields(self, payloadDic):
        dic = payloadDic['Transaction']
        info_dic = dic['info']
        flag = True
        transAllowedAmount = ds.maxAmountdict[info_dic['consumer_name'] + '-' + dic['Payment_Reciever']]
        if len(dic['country_id']) != 2 or dic['country_id'] not in ds.supportedCountries: flag = False
        if len(dic['currency_id']) != 3 or dic['currency_id'] not in ds.supportedCurrines: flag = False
        if info_dic['consumer_name'] + '-' + dic['Payment_Reciever'] not in ds.maxAmountdict: flag = False
        if int(dic['amount']) < 0: flag = False
        if int(dic['amount']) > int(transAllowedAmount): flag = False
        if not checkcredit.check_valid_card(card_number=info_dic['CreditCardNumber'],
                                            card_cvv=info_dic['ccv']): flag = False
        if not checkBank(info_dic['consumer_bank'], info_dic['bank_code']): flag = False
        if not checkAccountNumber(info_dic['account_number'], info_dic['consumer_bank'], info_dic['CreditCardNumber'],
                                  dic['country_id']): flag = False

        return flag


if __name__ == "__main__":
    pass
