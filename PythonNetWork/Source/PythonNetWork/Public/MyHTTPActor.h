// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Interfaces/IHttpRequest.h"
#include "MyHTTPActor.generated.h"

UENUM(BlueprintType)
enum class EDataID
{
	EID_UserData, // UMETA()
};

USTRUCT(BlueprintType)
struct FDataField
{
	GENERATED_BODY()

	EDataID DataID;
	TArray<FString> StringFields;
};

UCLASS()
class PYTHONNETWORK_API AMyHTTPActor : public AActor
{
	GENERATED_BODY()
	
public:
	UFUNCTION()
	void MyHttpCall(EDataID ID, const TArray<FString>& StringFields, const FString& URL); // http 요청에 사용할 함수
	
	// http GET 요청 직후 호출되는 콜백함수
	void OnResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful);

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

private:
	static void GetDataJson(TArray<FString>& Result, FString JsonSource);
	void ExportJsonData(const FString& JsonData, TSharedPtr<FJsonObject> JsonObject);
	FDataField DataField;

	UPROPERTY()
	class UMyHTTPWidget* CoinWidget;

	UPROPERTY(EditDefaultsOnly)
	TSubclassOf<UUserWidget> CoinWidgetFactory;
};
