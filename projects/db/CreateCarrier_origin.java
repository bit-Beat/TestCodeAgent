public class CreateCarrier extends AbstractTransactionCaller {

	public CreateCarrier(Transaction txn, String bizId){
		super(txn, bizId);
	}
	
	@Override
	public void execute(Document doc) throws SQLException, SystemException, BizException{
		String strCarrierId = MessageUtil.getBodyItemValue(doc, "CarrierId");
		String strCarrierType = MessageUtil.getBodyItemValue(doc, "CarrierType");
		String strCarrierSpec = MessageUtil.getBodyItemValue(doc, "CarrierSpec");
		String strCategory = MessageUtil.getBodyItemValue(doc, "Category");
		String strSubCategory = MessageUtil.getBodyItemValue(doc, "SubCategory");
		String strMaterial = MessageUtil.getBodyItemValue(doc, "Material");
		String strTimeUsedLimit = MessageUtil.getBodyItemValue(doc, "TimeUsedLimit");
		String strDurationUsedLimit = MessageUtil.getBodyItemValue(doc, "DurationUsedLimit");
		String strCleanDurationUsedLimit = MessageUtil.getBodyItemValue(doc, "CleanDurationUsedLimit");
		String strCleanTimeUsedLimit = MessageUtil.getBodyItemValue(doc, "CleanTimeUsedLimit");
		String strCleanTimeLimit = MessageUtil.getBodyItemValue(doc, "CleanTimeLimit");
		String strOperator = MessageUtil.getBodyItemValue(doc, "Operator");

		if (strCarrierId.length() == 0 || strCarrierType.length() == 0 || strCarrierSpec.length() == 0 || strCategory.length() == 0 || strSubCategory.length() == 0 || strMaterial.length() == 0 || strTimeUsedLimit.length() == 0 || strDurationUsedLImit.length() == 0 || strCleanDurationUsedLimit.length() == 0 || strCleanTimeUsedLimit.length() == 0 || strCleanTimeLimit.length() == 0 || strOperator.length() == 0) { ErrorMessageBuilder.throwException(BizErrorCode,MES_ESSENTIAL_INPUT_ERROR, "11002", FacLangTypeCnst.getFacLangType(), null, strCarrierId, strCarrierType, strCarrierSpec, strCategory, strMaterial, strTimeUsedLimit, strDurationUsedLimit, strCleanDurationUsedLimit, strCleanTimeUsedLimit, strCleanTimeLimit, strOperator); }

		@SuppressWarnings("unused")
		DurableMasterInfo Durable = new DurableMasterInfo();

		try {
			Durable = this.getDurableManager().selectByName(MessageUtil.getBodyItemValue(doc, "CarrierId"));
			ErrorMessageBuilder.throwException(BizErrorCode.NT_DURABLE_DUPLICATE, "1", FacLangTypeCnst.getFacLangType(), null, MessageUtil.getBodyItemValue(doc, "CarrierId"));}
		catch (NotFoundSignal e1) {
			logger.debug(e1);

			try {
				getCarrierTrx().createCarrier(doc);
			} catch (Exception e) {
				ErrorMessageBuilder.throwException(doc);
			}
		}

		MessageUtil.setResultItemValue(doc, MessageUtil.Result_ReturnCode, "0");
		StringBuilder SendMessage = new StringBuilder();
		SendMessage.append("CarrierId=");
		SendMessage.append(MessageUtil.getBodyItemValue(doc, "CarrierId"));

		this.replyExecute(MessageUtil.getHeaderItemValue(doc, "ReplySubjectName"), SendMessage.toString(), ReplyFormatter.class, doc);
	}
}
	
	






















		
