// Fill out your copyright notice in the Description page of Project Settings.


#include "MyHTTPActor.h"

#include "HttpModule.h"
#include "Blueprint/UserWidget.h"
#include "Interfaces/IHttpResponse.h"
#include "MyHTTPWidget.h"
#include "Components/TextBlock.h"


// Called when the game starts or when spawned

void AMyHTTPActor::BeginPlay()
{
	//TArray<FString> StringFields = {"id", "name", "email"};
	
	//DataField.DataID = EDataID::EID_UserData;
	//DataField.StringFields = StringFields;
	
	//MyHttpCall(EDataID::EID_UserData, StringFields,"http://127.0.0.1:8000/users/");

	TArray<FString> StringFields = {"name", "drinkCan", "dollarPrice", "realtimeBTC", "realtimeETH", "realtimeSOL", "realtimeXRP",
									"realtimeDOGE", "BTCforDollar", "ETHforDollar", "SOLforDollar", "XRPforDollar", "DOGEforDollar"};
	
	DataField.DataID = EDataID::EID_UserData;
	DataField.StringFields = StringFields;
	
	MyHttpCall(EDataID::EID_UserData, StringFields,"http://127.0.0.1:8000/coins/");
	
	
	Super::BeginPlay();

	if(CoinWidgetFactory)
	{
		CoinWidget = CreateWidget<UMyHTTPWidget>(GetWorld(), CoinWidgetFactory);
		CoinWidget->AddToViewport();
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("UI 생성 못함."));
	}

}


void AMyHTTPActor::MyHttpCall(EDataID ID, const TArray<FString>& StringFields, const FString& URL)
{
	DataField.DataID = ID;
	DataField.StringFields = StringFields;
	
	auto& Http = FHttpModule::Get();
	const TSharedRef<IHttpRequest> Request = Http.CreateRequest();

	Request->OnProcessRequestComplete().BindUObject(this, &AMyHTTPActor::OnResponseReceived);
	
	Request->SetURL(URL);
	
	Request->SetVerb("GET");
	Request->SetHeader("Content-Type", TEXT("application/json"));
	Request->ProcessRequest();
}

void AMyHTTPActor::OnResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
	if (!Response.IsValid())
	{
		// 응답이 유효하지 않음
		return;
	}

	const int32 ResponseCode = Response->GetResponseCode();
	const FString ResponseContent = Response->GetContentAsString();

	// 응답이 성공적으로 받아졌고, 상태 코드가 200인 경우
	if (bWasSuccessful && ResponseCode == 200)
	{
		TArray<FString> JsonReader;
		GetDataJson(JsonReader, ResponseContent);
		
		// JSON 파싱 예시 (JSON 파서를 사용하여 실제로는 파싱해야 함)
		const TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);

		// 배열로 담겨진 JsonData 들을 재배치 시킨다.
		for(FString elem : JsonReader)
			ExportJsonData(elem, JsonObject);

	}
	else
	{
		// 응답이 실패하거나 상태 코드가 200이 아닌 경우
		UE_LOG(LogTemp, Error, TEXT("Failed to receive valid response. Response code: %d"), ResponseCode);
	}
}


void AMyHTTPActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
}

void AMyHTTPActor::GetDataJson(TArray<FString>& Result, FString JsonSource)
{
	if(JsonSource.Len() < 4)
	{
		UE_LOG(LogTemp, Error, TEXT("Response is empty."));
		return;
	}
		
	TCHAR C = JsonSource[3];
	FString Str;
		
	int32 Depth = 0;

	for (TCHAR Char : JsonSource)
	{
		if (Char == '{')
			Depth++;
			
		else if (Char == '}')
			Depth--;
			
		else if (Char == ',' && Depth == 0)
		{
			Str.InsertAt(0, '{');
			Str.InsertAt(Str.Len(), '}');
			Result.Add(Str);
			Str = "";
		}
		else if(Char != ']' && Char != '[')
			Str += Char;
	}
		
	if(Str.Len())
	{
		Str.InsertAt(0, '{');
		Str.InsertAt(Str.Len(), '}');
		Result.Push(Str);
	}
}

void AMyHTTPActor::ExportJsonData(const FString& JsonData, TSharedPtr<FJsonObject> JsonObject)
{
	const TSharedRef<TJsonReader<TCHAR>> Reader = TJsonReaderFactory<TCHAR>::Create(JsonData);
	
	if (FJsonSerializer::Deserialize(Reader, JsonObject))
	{
		for(const auto& elem : DataField.StringFields)
		{
			FString DataValue;
			if (JsonObject->TryGetStringField(elem, DataValue))
			{
				if(elem == L"name") CoinWidget->name->SetText(FText::FromString(DataValue));
				if(elem == L"drinkCan") CoinWidget->drinkCan->SetText(FText::FromString(DataValue));
				if(elem == L"dollarPrice") CoinWidget->dollarPrice->SetText(FText::FromString(DataValue));
				if(elem == L"realtimeBTC") CoinWidget->realtimeBTC->SetText(FText::FromString(DataValue));
				if(elem == L"realtimeETH") CoinWidget->realtimeETH->SetText(FText::FromString(DataValue));
				if(elem == L"realtimeSOL") CoinWidget->realtimeSOL->SetText(FText::FromString(DataValue));
				if(elem == L"realtimeXRP") CoinWidget->realtimeXRP->SetText(FText::FromString(DataValue));
				if(elem == L"realtimeDOGE") CoinWidget->realtimeDOGE->SetText(FText::FromString(DataValue));
				if(elem == L"BTCforDollar") CoinWidget->BTCforDollar->SetText(FText::FromString(DataValue));
				if(elem == L"ETHforDollar") CoinWidget->ETHforDollar->SetText(FText::FromString(DataValue));
				if(elem == L"SOLforDollar") CoinWidget->SOLforDollar->SetText(FText::FromString(DataValue));
				if(elem == L"XRPforDollar") CoinWidget->XRPforDollar->SetText(FText::FromString(DataValue));
				if(elem == L"DOGEforDollar") CoinWidget->DOGEforDollar->SetText(FText::FromString(DataValue));
				
				UE_LOG(LogTemp, Warning, TEXT("Received data from server: %s"), *DataValue);
			}
		}
	}
}


