// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "MyHTTPWidget.generated.h"

/**
 * 
 */
UCLASS()
class PYTHONNETWORK_API UMyHTTPWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	UPROPERTY(meta=(BindWidget))
	class UTextBlock* name;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* drinkCan;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* dollarPrice;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* realtimeBTC;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* realtimeETH;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* realtimeSOL;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* realtimeXRP;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* realtimeDOGE;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* BTCforDollar;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* ETHforDollar;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* SOLforDollar;

	UPROPERTY(meta=(BindWidget))
	UTextBlock* XRPforDollar;
	
	UPROPERTY(meta=(BindWidget))
	UTextBlock* DOGEforDollar;
	
};
