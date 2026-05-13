@Nested
@DisplayName("NEW_ENGT_FOUP 생성/수정/삭제 테스트")
public class NEW_ENGT_FOUP_Test
{
	@DisplayName("FOUP신규 생성 시 Type이 Engineer이면서 SubType이 enum에 추가 되어있는 type인 경우 durableattr 테이블 값 생성확인 CreateNEW_ENGT_FOUP")
	@FlagOn("AD_20250827_NewEngtFoupAttributeManage")
	public void CreateNEW_ENGT_FOUP(String carrierId, String category, String subCategory) throws Exception{
		StringBuilder query = new StringBuilder();
		ArrayList<Object> aBindInfo = new ArrayList<Object>();
		String foupCreateMessage = String.join(
			COMMAND_START
			,"CreateCarrier", "CarrierId=:CarrierId", "CarrierType=FOUP", "CarrierSpec=FOUP", "Category=:Category", "SubCategory=:SubCategory", "Material=Material", "TimeUsedLimit=1000", "DurationUsedLimit=3652", "CleanDurationUsedLimit=365"
, "CleanTimeUsedLimit=1000", "CleanTimeLimit=1000", "Operator=X0158599"
		);

		Given(foupCreateMessage)
		.When((param) -> {
			param.put("CarrierId", carrierId);
			param.put("Category", category);
			param.put("SubCategory", subCategory);
			return param;
		})
		.Then(result -> {
			String[][] queryReulst = null;
			query.setLength(0);
			query.append("SELECT * FROM BIZ_DURABLEATTR_DET WHERE ATTR_NM = 'NEW_ENGT_FOUP' AND DURABLE_ID = ? AND ATTR_VAL = ?");
			aBindInfo.clear();
			aBindInfo.add(carrierId); 
			aBindInfo.add(subCategory);
			queryResult = getTxn().selectForSetArray(query.toString(), getDoc(), aBindInfo);

			assertNotNull(queryResult);
			assertTrue(queryResult.length > 0);

			if(queryResult.length > 0)
				System.out.println("Success");
			else
				System.out.println("Fail");
		}
	}
}