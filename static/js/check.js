//------------------表单校验
$(function(){
	$("#wizard").scrollable({
		onSeek: function(event,i){
			$("#status li").removeClass("active").eq(i).addClass("active");
		},
		onBeforeSeek:function(event,i){
			if(i==1){
				var house_address = $("#house_address").val();
				if(house_address==""){
					alert("请输入房屋地址！");
					return false;
				}
			}
			if(i==2){
				var house_area = $("#house_area").val();
				if(house_area==""){
					alert("请输入房屋面积！");
					return false;
				}
				var bedroom_numbers = $("#bedroom_numbers").val();
				if(bedroom_numbers==""){
					alert("请输入卧室数量！");
					return false;
				}
				var bed_numbers = $("#bed_numbers").val();
				if(bed_numbers==""){
					alert("请输入床数量！");
					return false;
				}
				var toilet_numbers = $("#toilet_numbers").val();
				if(toilet_numbers==""){
					alert("请输入卫生间数量！");
					return false;
				}
			}
			if(i==3){
				var house_tilte = $("#house_tilte").val();
				if(house_tilte==""){
					alert("请输入房间主题！");
					return false;
				}
				var house_deenption = $("#house_deenption").val();
				if(house_deenption==""){
					alert("请输入房屋描述！");
					return false;
				}
			}
			if(i==4){
				var use_rule = $("#use_rule").val();
				if(use_rule==""){
					alert("请输入使用规则！");
					return false;
				}
			}
//					if(i==5){
//						var use_rule = $("#use_rule").val();
//						if(use_rule==""){
//							alert("请上传房屋照片！");
//							return false;
//						}
//					}
			if(i==6){
				var house_price = $("#house_price").val();
				if(house_price==""){
					alert("请输入房屋价格！");
					return false;
				}
				var min_days = $("#min_days").val();
				if(min_days==""){
					alert("请输入最少起住天数！");
					return false;
				}
				var max_days = $("#max_days").val();
				if(max_days==""){
					alert("请输入最大入住天数！");
					return false;
				}
				if (min_days>max_days){
					alert("最大入住天数应该大于最少起住天数!");
					return false;
				}
			}
		}
	});
//-------------------------点击提交代码之后显示提交的信息并返回主界面
	$("#sub").click(function(){
		var data = $("form").serialize();
		alert(data);
		//window.open("../HomePage/userHomePage.html")
	});
});
$(function () { $("[data-toggle='tooltip']").tooltip({html : true }); });