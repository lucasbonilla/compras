help:
	@clear
	@echo ""
	@echo ""
	@echo "                                                                        #,********"
	@echo "                                                                     //(///////////"
	@echo "                                                                     **/*,"
	@echo "                   (////////////////////////////////////////////////**&%/"
	@echo "                   ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,&@"
	@echo "                    *//,*///,/,//////*///////,/////,//////(/*////,//*(#&"
	@echo "                    &//,&    /,     **      /.     **     ,/#    ,//,@&"
	@echo "                     *//*****//*****//******//*****//*****//*****//*/#@"
	@echo "                     ./*,    .*,    .*#     *.     *,    **,    ,*/,&%/"
	@echo "                      ***#####*(#####*######*(#####*/#####*(####****&@"
	@echo "                      ,**,,,,,**,,,,,*.,,,,,*,,,,,.*,,,,,,*,,,,,**,(#&"
	@echo "                      #,,,    .,,    ,,     ,.    .,    ,,.    .**.@&"
	@echo "                       ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,/#@"
	@echo "                       .,,,    ,,#   .,     ,.    ,,    ,,    ,,,.%%*"
	@echo "                        ,,,    (,,   ,,/    ,.    ,.   ,,.   &,,,/%@"
	@echo "                        .,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.&%&"
	@echo "                       *((((((((((((((((((((((((((((((((((((((#@%@*"
	@echo "                                                                 %/&."
	@echo "                                                                  *%#*"
	@echo "                     %#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#&@#/"
	@echo "                           *,**,,,                     .,**,,."
	@echo "                         .../@%(/.,                  ...(@%(/./"
	@echo "                         .,, #&*,,,                 ..,, #&,,,,"
	@echo "                          ,,////.,                  / ,,////,,"
	@echo "                           & ...,                      / .. *"
	@echo ""
	@echo ""
	@echo ""
	@echo "Persistência de uma arquivo .txt em uma base de dados PostgreSQL."
	@echo "Todos os comandos usam docker-compose"
	@echo ""
	@echo "Utilização: make [comando]"
	@echo "\tComandos: "
	@echo "\t\tdown"
	@echo "\t\t\t- Destrói todos os conteiners"
	@echo "\t\tbuild"
	@echo "\t\t\t- Constrói todos os conteiners"
	@echo "\t\tup"
	@echo "\t\t\t- Carrega a aplicação (pode demorar um tempo na primeira execução :S )"
	@echo "\t\tlogs"
	@echo "\t\t\t- Mostra os logs dos serviços"
	@echo "\t\tbuild-up"
	@echo "\t\t\t- Constrói todos os conteiners"
	@echo "\t\t\t- Carrega a aplicação"

down:
	@docker-compose down
	
build:
	@docker-compose build
	
up:
	@docker-compose up -d

build-up:
	@docker-compose build && docker-compose up -d
	
logs:
	@docker-compose logs -f