;; N concurrent GETs to a local server; count the 200s. java.net.http + futures.
(import '[java.net.http HttpClient HttpRequest HttpResponse$BodyHandlers]
        '[java.net URI])
(def n (Long/parseLong (or (System/getenv "BENCH_N") "100")))
(def port (or (System/getenv "BENCH_HTTP_PORT") "8089"))
(def url (str "http://127.0.0.1:" port "/"))
(def client (HttpClient/newHttpClient))
(defn fetch [_]
  (try
    (let [req (.build (.uri (HttpRequest/newBuilder) (URI/create url)))
          resp (.send client req (HttpResponse$BodyHandlers/ofString))]
      (if (= 200 (.statusCode resp)) 1 0))
    (catch Exception _ 0)))
(println (reduce + (map deref (doall (map (fn [i] (future (fetch i))) (range n))))))

;; Stop the agent/future thread pool so the JVM exits promptly (else it lingers ~60s).
(shutdown-agents)
