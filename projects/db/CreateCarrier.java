public class CreateCarrier extends AbstractTransactionCaller {

	private final Transaction txn;

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
				if (getCOMTrx().getFabUseYN("AD_20250827_NewEngtFoupAttributeManage", doc))
				{
					createNewEngtFoup(doc);
				}
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

	public void createNewEngtFoup(Document doc) throws SQLException, BizException {
		String carrierId = MessageUtil.getBodyItemValue(doc, "CarrierId");
		String category = MessageUtil.getBodyItemValue(doc, "Category");
		String subCategory = MessageUtil.getBodyItemValue(doc, "SubCategory");

		StringBuilder query = new StringBuilder();
		HashMap<String, Object> aBindSetInfo = new HashMap<String, Object>();
		String[][] arrResult = null;

		if(category.equals("Engineer"))
		{
			query.setLength(0);
			query.append("SELECT TYP_VAL FROM MES_COMMONTYP_DET WHERE COMMON_TYP = :COMMON_TYP AND TYP_VAL = :TYP_VAL AND DEFAULT_YN ='Y'");
		
			aBindSetInfo.clear();
			aBindSetInfo.put("COMMON_TYP", "NEW_ENGT_FOUP");
			aBindSetInfo.put("TYP_VAL", subCategory);

			try { arrResult = this.getTransaction(). selectForStrArray(query. toString(), doc, aBindSetInfo); }
			catch (Exception e){
				logger.debug("[NewEngtFoup ENUM 테이블 조회 중 에러 발생!]"+e);
				return;
			}
		
			if(arrResult.length == 0) return;
			
			logger.info("DURABLE_ID : " + carrierId+", ATTR_NM : NEW_ENGT_FOUP, ATTR_VAL : "+subCategory+" Insert Start!");
			//DurableManagement durableMgmt = new DurableManagement(this);
			setDurableAttr(carrierId, "NEW_ENGT_FOUP", subCategory);
			logger.info("DUABLE_ID: "+carrierId+", ATTR_NM : NEW_ENGT_FOUP, ATTR_VAL : "+subCategory+" Insert Complete!");
		}
		else return;
	}
	
	public void setDurableAttr(String carrierId, String attrNm, String attrVal) throws SQLException
	{
		
		String sQuery = "";
		sQuery += "MERGE INTO BIZ_DURABLEATTR_DET A ";
		sQuery += "USING DUAL ";
		sQuery += "    ON (A.DURABLE_ID = ? AND A.ATTR_NM = ?) ";
		sQuery += "WHEN MATCHED THEN ";
		sQuery += "    UPDATE SET ATTR_VAL = ? ";
		sQuery += "WHEN NOT MATCHED THEN ";
		sQuery += "    INSERT (DURABLE_ID, ATTR_NM, ATTR_VAL) VALUES (?, ?, ?)";

		ArrayList<Object> aBindSetInfo = new ArrayList<Object>();
		aBindSetInfo.clear();
		aBindSetInfo.add(carrierId);
		aBindSetInfo.add(attrNm);
		aBindSetInfo.add(attrVal);
		aBindSetInfo.add(carrierId);
		aBindSetInfo.add(attrNm);
		aBindSetInfo.add(attrVal);

		txn.merge(sQuery, aBindSetInfo);
	}
}
	
	






















		
