<?php
// ====================================================================
// CONFIGURAZIONE E FUNZIONI DI SUPPORTO
// ====================================================================

// Configurazione del servizio SRL (deve essere accessibile dal server PHP!)
$SRL_SERVICE_URL = 'http://'.getenv('SRL_HOST').':'.getenv('SRL_PORT');

// Funzione helper per ottenere l'IP VPN (come simulato in index.php)
function getVPNIP() {
    // In un sistema reale, questo dovrebbe provenire dalla sessione o da un meccanismo di autenticazione
    return "10.8.0.2"; // Valore fittizio di esempio
}

// Funzione helper per le chiamate API
function safeFetchJSON($url, $method = 'GET') {
    global $SRL_SERVICE_URL;
    $fullUrl = strpos($url, 'http') === 0 ? $url : $SRL_SERVICE_URL . $url;

    // Utilizzo di cURL per una gestione più robusta delle richieste HTTP
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $fullUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method); // Setta il metodo (PUT, PATCH, GET, etc.)
    curl_setopt($ch, CURLOPT_TIMEOUT, 5); // Timeout di 5 secondi
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    if (curl_errno($ch)) {
        error_log("cURL Error for $fullUrl: " . curl_error($ch));
        curl_close($ch);
        return null;
    }
    curl_close($ch);

    if ($httpCode !== 200) {
        error_log("HTTP Error for $fullUrl: Code $httpCode");
        return null;
    }

    $data = json_decode($response, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        error_log("JSON Decode Error for $fullUrl: " . json_last_error_msg());
        return null;
    }
    
    return ['success' => true, 'data' => $data, 'http_code' => $httpCode];

}



// ====================================================================
// LOGICA DI GESTIONE DELLE AZIONI
// ====================================================================

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    
    $action = $_POST['action'];
    $vpnIp = getVPNIP();
    $redirectStatus = 'error'; // Default in caso di fallimento

    switch ($action) {
        case 'disconnect':
            $result = safeFetchJSON("/api/user/{$vpnIp}/disconnect", 'PUT');
            if ($result['success']) {
                $redirectStatus = 'disconnected';
            }
            break;

        case 'set_available':
            $result = safeFetchJSON("/api/service/availability/true", 'PATCH');
            if ($result['success']) {
                $redirectStatus = 'availability_true';
            }
            break;

        case 'set_unavailable':
            $result = safeFetchJSON("/api/service/availability/false", 'PATCH');
            if ($result['success']) {
                $redirectStatus = 'availability_false';
            }
            break;
            
        default:
            // Azione non riconosciuta
            $redirectStatus = 'error';
            break;
    }

    // Reindirizza alla dashboard principale con lo stato aggiornato
    header("Location: index.php?status=" . $redirectStatus);
    // header("Location: index.php");
    exit;

} else {
    // Metodo non POST o campo 'action' mancante
    header("Location: index.php?status=error_invalid_request");
    exit;
}
?>

