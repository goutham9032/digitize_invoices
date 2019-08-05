$DOM = $(document)
$DOM.ready(function(){

    function call_ajax(url, type, data) {
         data = data || '';
         var request = $.ajax({
                             type: type,
                             url: url,
                             data:data,
                       });
         return request;
    }

    function file_upload(){
       $('#upload_file').prop('disabled',false);
       $('#download_btn').remove();
    }

    function reset_file_ip(){
        $('#ip_file').val('');
        $('#upload_file .fa-spinner').addClass('no_display');
        $('#upload_file .glyphicon-upload').html('Upload File');
    }

    function upload_file(){
        $('#upload_file .glyphicon-upload').html('Uploading')
        $('#upload_file .fa-spinner').removeClass('no_display')
        event.preventDefault();
        var request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if(this.readyState === 4  && this.status == 200 && this.responseText.includes('true')){
                reset_file_ip()
                alertify.success('File uploaded successfully');
                $('#upload_file').prop('disabled', true);
		        window.location.href = location.pathname; 
            }
            else if(this.responseText.includes('false')){
                if(!$(".alertify-notifier .ajs-error").is(':visible')){
                   reset_file_ip()
                   alertify.error('File uploading failed');
                }
            } 
        }
		request.open('POST', '/', true);
        var formData = new FormData(document.getElementById('file_upload_form'));
        request.send(formData);
    }

    function save_update_invoice(){
        var data = { 'file_id':location.pathname.split('/')[2],
                     'invoice_no':$('#invoice_no').val(),
                     'from':$('#from').val(),
                     'to':$('#to').val(),
                     'date':$('#date').val()
                   }
        req = call_ajax(location.pathname, 'POST', JSON.stringify(data));
	    $.when(req).done(function(data) {
		   if(data.success){
		      window.location.href = location.pathname; 
		   }
	    });
       
    }

    function digitize_invoice(){
        req = call_ajax('/digitize/' + location.pathname.split('/')[2], 'GET');
	    $.when(req).done(function(data) {
		   if(data.success){
		      window.location.href = location.pathname; 
		   }
	    });
    }

    function bindEvents() {
        $DOM.on('change', '#ip_file', file_upload)
            .on('click', '#upload_file', upload_file)
            .on('click', '#save_update', save_update_invoice)
            .on('click', '#digitize', digitize_invoice)
    }
    
    alertify.set('notifier', 'position', 'top-right');
    bindEvents();

});
