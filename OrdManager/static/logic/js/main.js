$(document).ready(function(){

    $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
    });
    var buyerPk = 0;
    if (sessionStorage.getItem('person')){
        buyerPk = parseInt(sessionStorage.getItem('person'));
        var idOnClickPrevious = "#" + buyerPk;
        var idOnClickOrdList = '#ord' + buyerPk;
        $(idOnClickPrevious).css('background-color', '#AFEEEE');
        $(idOnClickOrdList).css('display', 'block');
    };
    $('.staff').click(function(){
        var idOnClickPrevious = "#" + buyerPk;
        var idOnClickOrdList = '#ord' + buyerPk;
        $(idOnClickPrevious).css('background-color', 'white');
        $(idOnClickOrdList).css('display', 'none');
        buyerPk = $(this).data('pk');
        var idOnClickOrdList = '#ord' + buyerPk;
        $(this).css('background-color', '#AFEEEE');
        $(idOnClickOrdList).css('display', 'block');
        console.log(buyerPk);
    });
    var groupId = '';
    $('.groupProd').click(function(){
        var group = $(this).data('group');
        var OnClickGroup = "#" + group;
        var OnClickGroupPrevious = "#" + groupId;
        if (groupId != ''){
            $(OnClickGroupPrevious).css('display', 'none');
            };
        groupId = group;
        $(OnClickGroup).css('display', 'block');
    });
    var buyPrice = 0;
    var buyName = 0;
    var buyPk = 0;
    $('.products').click(function(){
        var id = $(this).data('buyid');
        var idOnClick = '#buy' + id;
        var idOnClickPrevious = '#buy' + buyPk;
        $(idOnClickPrevious).css('background-color', 'white');
        $(idOnClick).css('background-color', '#AFEEEE');
        buyPrice = $(this).data('buyprice');
        buyName = $(this).data('buyname');
        buyPk = id;
        console.log(buyPrice, buyName, buyPk);
    });
    $('.add').click(function(){
        var url = '/addbuy/';
        if(buyerPk != 0 && buyPk != 0){
            var data = {
                'buyId': buyPk,
                'buyer_id': buyerPk,
                'name': buyName,
                'price': buyPrice
            };
            $.ajax({url: url,
                data: data,
                type: 'POST',
                success: function(){
                sessionStorage.setItem("person", String(buyerPk))
                location.reload();
            }
            });
        }
        else{
            if(buyerPk == 0){
                alert('Выберете покупателя из списка');
            }
            else{
                alert('Выберете блюдо из списка');
            }
        }
    });
    $(window).on("beforeunload", function() {
        sessionStorage.setItem("person", String(buyerPk))
    });
    $('.deleteOrder').click(function(){
        var url = '/addbuy/';
        var idToDell = $(this).data('pk');
        var data = {
            'id': idToDell,
        };
        var to_hide = "#order" + idToDell;
        console.log(to_hide)
        $.ajax({url: url,
            data: data,
            type: 'DELETE',
            success: function(){
            $(to_hide).css('display', 'none');
            }
        });
    });
        $('.amount').blur(function(){
        var url = '/addbuy/';
        var newAmount = $(this).val();
        var idToChangeAmount = $(this).data('pk');
        var data = {
            'id': idToChangeAmount,
            'amount': newAmount,
        };
        $.ajax({url: url,
            data: data,
            type: 'PATCH',
            success: function(){
            }
        });
    });
      $('.updatestaff').click(function(){
          var idUpdate = $(this).data('pk');
          var idOnClickToUpdateFormActive = '#updateform' + idUpdate;
          if ($(idOnClickToUpdateFormActive).css('display') == 'none') {$(idOnClickToUpdateFormActive).css('display', 'block')}
              else {$(idOnClickToUpdateFormActive).css('display', 'none')}
          });
      $('.saveNewNameData').click(function(){
            var idUpdatePk = $(this).data('pk');
            var idOnClickToUpdateFormActive = '#updateform' + idUpdatePk;
            var newName = '#name' + idUpdatePk;
            var newSurname = '#surname' + idUpdatePk;
            var newSecondName = '#secondname' + idUpdatePk;
            newName = $(newName).val();
            newSurname = $(newSurname).val();
            newSecondName = $(newSecondName).val();
            var url = '/changestaff/';
            var data = {
                'id': idUpdatePk,
                'name': newName,
                'surname': newSurname,
                'secondname': newSecondName,
            };
            $.ajax({url: url,
                data: data,
                type: 'PATCH',
                success: function(){
                var newNameString = newSurname + " " + newName + " " + newSecondName
                var idNameChange = '#' + idUpdatePk
                $(idNameChange).text(newNameString)
                $(idOnClickToUpdateFormActive).css('display', 'none')
                }
        });
            return false;
       });
      $('.dellstaff').click(function(){
        var url = '/changestaff/';
        var data = {
            'id': buyerPk,
        };
        var to_hide = "#element" + buyerPk;
        $.ajax({url: url,
            data: data,
            type: 'DELETE',
            success: function(){
            $(to_hide).css('display', 'none');
            }
        });
    });
     $('.addNewEmployee').click(function(){
         if ($('.formToAdd').css('display') == 'none') {$('.formToAdd').css('display', 'block')}
         else {$('.formToAdd').css('display', 'none')}
      });
      $('.confirm').click(function(){
        var url = '/addbuy/';
        var companyToConfirm = $(this).data('user');
        var data = {
            'companyid': companyToConfirm,
        };
        $.ajax({url: url,
            data: data,
            type: 'PATCH',
            success: function(){
            $('.status').text('Подтвержден')
            }
        });
        });
      $('.dellbyperson').click(function(){
        var url = '/addbuy/';
        var idOnClickOrdList = '#ord' + buyerPk;
        var data = {
            'buyerToDell': buyerPk,
        };
        $.ajax({url: url,
            data: data,
            type: 'DELETE',
            success: function(){
            $(idOnClickOrdList).remove();
            }
        });
        });
       $('.dellall').click(function(){
        var url = '/addbuy/';
        var companyToConfirm = $(this).data('user');
        console.log(companyToConfirm)
        var data = {
            'companyid': companyToConfirm,
        };
        $.ajax({url: url,
            data: data,
            type: 'DELETE',
            success: function(){
            $('.orderAllStaff').remove();
            }
        });
        });
});