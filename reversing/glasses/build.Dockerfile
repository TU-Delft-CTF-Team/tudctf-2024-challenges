FROM mcr.microsoft.com/dotnet/sdk AS builder

WORKDIR /no/flag/here/sorry
COPY Glasses ./Glasses
RUN dotnet build Glasses --configuration Release

FROM scratch AS output

WORKDIR /output
COPY --from=builder /no/flag/here/sorry/Glasses/bin/Release/net481/Glasses.exe /output/Glasses.exe