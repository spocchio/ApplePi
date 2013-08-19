var baseurl="/" 
var currentApp = null
var currentId = null
var currentMethod=null
 function call(object,self,method,parameters,f){
	 $.ajax({
		
		url:baseurl+object+'/'+self+'/'+method,
		data: parameters,
		success: function(res){
			f(res)
			}
	});

 }

function callJSON(object,self,method,parameters,f){

	call(object,self,method,parameters, function(res){ 
		jres=JSON.parse(res)
		f(jres)
	})
}
function readHTML(method,parameters,ele,f){
	call(currentApp,currentId,method,parameters,function(res) {
			if(ele!=null){
				$(ele).html(res)
				if(f!=undefined){
					f()
				}
			}
		}
	);
}
 function fileBrowser(ele,f){
	 divo=$('<div style="border:1px solid black;background-color:white;padding:2px;border-radius:2px;" ></div>')
  $(ele).after(divo);
	divo.fileTree({  folderEvent: 'click', expandSpeed: 750, collapseSpeed: 750, multiFolder: false }, function(file) { 
						f(file)
					});
	return false;
 }
  function fileBrowserFromHidden(ele){
	if ( $(ele).data('browser') == undefined || $(ele).data('browser')==false){
		$(ele).data('browser',true)
		fileBrowser(ele,function(file){
			$(ele).val(file)
		})
	}
	return false;
 }
 function reloadApp(app,self,method){
	 loadApp(currentApp,currentId,currentMethod)
 }
 function loadApp(app,self,method){
	 currentApp = app
	 currentId = self
	 currentMethod = method
	 call(app,self,method,{},function(data){
			
			$('#app').html(data);
			loadAppManager()
			loaded()
		 })
	 
 }
 function loaded(){
	 $("body").removeClass("loading"); 
 }
 function loading(){
	 $("body").addClass("loading"); 
	 }
 function loadAppManager(){
	 callJSON('AppManager','','appList',{}, function(ress){ 
		 $('#AppManagerUl').html('')
		 console.debug('applicazioni:')
		 console.debug(ress)
			for (var res in ress){
				names = ress[res];
				
				if (names==null){
					link = $("<a href='#'>[o] "+res+"</a>");
					link.data('name',res);
					link.click(function(me){
							loading()
							loadApp($(this).data('name'),'','HTML')
					});
					ol2 = $('<ol></ol>')
				}else{
					link = $("<a href='#'>[+] "+res+"</a>");
					link.data('name',res);
					link.click(function(me){
						name = $(this).data('name')
						callJSON(name,'','',{}, function(id){ 
							loading()
							loadApp(name,id,'HTML')
						});
					});
					ol2 = $('<ol></ol>')
					for (var name in names){
						id = names[name]
						il2 = $('<li></li>')
						link2 = $("<a href='#'> ["+id+"]</a>");
						link2.data('name',res);
						link2.data('id',id);
						link2.click(function(me){
								loading()
								loadApp($(this).data('name'),$(this).data('id'),'HTML')
							
						});
						link3 = $("<a href='#'> [X] </a>");
						link3.data('name',res);
						link3.data('id',id);
						link3.click(function(me){
								loading()
								callJSON(link3.data('name'),link3.data('id'),'close',{'app':link3.data('name'),'id':link3.data('id')}, function(id){ 
									loadApp('AppManager','','HTML')
								});
								
							
						});
						il2.append(link3)
						il2.append("<span> </span>")
						il2.append(link2)
						ol2.append(il2)
						
					}
				}
				li=$("<li></li>");
				li.append(link)
				li.append(ol2)
				$('#AppManagerUl').append(li);
			}

		 })
 }
 function readFrom(ele,classe,method,parameter){
	 callHTML(classe,method,parameter, function(res){ $(ele).html(res) } );
	 
 }
function reloadEvery(classe,self,method,parmeters,idElem,t,f){
			setTimeout(function(){
				readHTML(method,parmeters,idElem,f)
				if(currentApp == classe && currentId == self){
					reloadEvery(classe,self,method,parmeters,idElem,t,f)
					
				}
			},t)
}
