// ==============================================
// ANA JAVASCRIPT DOSYASI
// ==============================================
// Bu dosya uygulamanın JavaScript kodlarını içerir.
// Basit ve anlaşılır fonksiyonlar kullanılmıştır.
// ==============================================

// Sayfa yüklendiğinde çalışacak kodlar
document.addEventListener('DOMContentLoaded', function() {
    // Sayfa hazır olduğunda bu fonksiyon çalışır
    console.log('Sınav Programı Uygulaması Yüklendi!');
    
    // Uyarı mesajlarını otomatik gizle
    hideAlertsAfterDelay();
});


// ==============================================
// UYARI MESAJLARINI OTOMATİK GİZLE
// ==============================================
function hideAlertsAfterDelay() {
    // Sayfadaki tüm uyarı mesajlarını bul
    var alerts = document.querySelectorAll('.alert');
    
    // Her uyarı için
    for (var i = 0; i < alerts.length; i++) {
        var alert = alerts[i];
        
        // 5 saniye sonra gizle
        setTimeout(function(alertElement) {
            alertElement.style.opacity = '0';
            alertElement.style.transition = 'opacity 0.5s';
            
            // Tamamen kaldır
            setTimeout(function() {
                alertElement.remove();
            }, 500);
        }, 5000, alert);
    }
}


// ==============================================
// FORM DOĞRULAMA
// ==============================================
function validateForm(formId) {
    // Formu bul
    var form = document.getElementById(formId);
    
    // Form bulunamadıysa
    if (!form) {
        console.log('Form bulunamadı: ' + formId);
        return false;
    }
    
    // Zorunlu alanları kontrol et
    var requiredFields = form.querySelectorAll('[required]');
    var isValid = true;
    
    for (var i = 0; i < requiredFields.length; i++) {
        var field = requiredFields[i];
        
        // Alan boş mu?
        if (field.value.trim() === '') {
            // Hata göster
            field.style.borderColor = 'var(--danger-color)';
            isValid = false;
        } else {
            // Normal kenarlık
            field.style.borderColor = 'var(--border-color)';
        }
    }
    
    return isValid;
}


// ==============================================
// SİLME ONAY DİYALOĞU
// ==============================================
function confirmDelete(itemName) {
    // Kullanıcıya sor
    var result = confirm(itemName + ' silinecek. Emin misiniz?');
    return result;
}


// ==============================================
// SAYFA YÜKLENİYOR GÖSTERGESİ
// ==============================================
function showLoading() {
    // Yükleniyor göstergesini göster
    var loader = document.getElementById('loading');
    if (loader) {
        loader.style.display = 'flex';
    }
}

function hideLoading() {
    // Yükleniyor göstergesini gizle
    var loader = document.getElementById('loading');
    if (loader) {
        loader.style.display = 'none';
    }
}


// ==============================================
// ARAMA FONKSİYONU (Tablo için)
// ==============================================
function searchTable(inputId, tableId) {
    // Arama kutusunu bul
    var input = document.getElementById(inputId);
    var filter = input.value.toUpperCase();
    
    // Tabloyu bul
    var table = document.getElementById(tableId);
    var rows = table.getElementsByTagName('tr');
    
    // Her satırı kontrol et
    for (var i = 1; i < rows.length; i++) {
        var row = rows[i];
        var cells = row.getElementsByTagName('td');
        var found = false;
        
        // Her hücreyi kontrol et
        for (var j = 0; j < cells.length; j++) {
            var cell = cells[j];
            if (cell) {
                var text = cell.textContent || cell.innerText;
                if (text.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        // Satırı göster veya gizle
        if (found) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    }
}

