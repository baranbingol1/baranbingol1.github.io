# Makine Öğrenmesinde Hiperparametre Optimizasyonu

Merhabalar, yeni blog yazıma hoşgeldiniz. Bugün hiperparametre optimizasyonu üzerine konuşacağız, umarım okuyanlara faydalı bir yazı olur!

1. Başlamadan önce bu yazıda üstünden geçeceklerimizi özetlemek gerekirse:
{:toc}

1. Hiperparametre vs parametre aralarındaki fark nedir ?
2. Hiperparametre optimizasyonu yöntemleri
3. Veri seti üzerinde örnek bir uygulama

## Hiperparametre vs parametre aralarındaki fark nedir ?

Aradaki farkı öğrenmek için iki farklı regresyon modelini inceleyelim.

Parametreler modelin veriden çıkardığı bilgiler sonucu güncellenen değerlerdir yani parametreleri algoritmanın kendisi öğrenir. Örneğin basit bir doğrusal regresyon denklemi 

$$y = \beta_0 + \beta_1x$$

şeklinde gösterilebilir. Bu denklemde $x$ bağımsız değişken $y$ tahmin etmeye çalıştığımız bağımlı değişken, $\beta_0$ ve $\beta_1$ modelin optimize edeceği parametrelerdir.Verilen verilere göre bir loss function eşliğinde doğrusal regresyon algoritması bu parametreleri optimize eder.

Hiperparametreler model eğitilmeye başlamadan önce bizim tarafımızdan değeri belirlenir ve modelin veriyi nasıl öğreneceğini belirler. Örneğin yukarıda bahsettiğimiz basit doğrusal regresyon modelinin daha kapsamlı öğrenmesini sağlamak için ridge regresyonu adı verilen başka bir regresyon algoritması kullanılabilir. Bu regresyonda ise kontrol etmemiz gereken bir hiperparametre olan lambda bulunur. Varsayalımki basit doğrusal regresyon modelimizin optimize etmeye çalıştığı loss function En Küçük Kareler fonksiyonu olsun 

$$L = \sum_{i=1}^n(y_i - \hat{y}_i)^2$$ 

bu denklemde n toplam veri noktalarının sayısı. $\hat{y}_i$ modelin tahmin ettiği y değeridir. $y_i$ ise gerçekte olan y değeridir. Modelimiz eğitildiği veri üzerinde gördüğü her bir değeri tahmin edecek ve tahmin sonucu bu loss functiondaki "skoruna" bakacaktır ve kendisini buna göre optimize edecektir. Yani yapmaya çalışacağı şey En Küçük Kareler fonksiyonunda 0'a ulaşmaktır. Ancak bunu yaparken modelimiz overfitting denilen bir sorunla karşılaşabilir bu da modelin eğittimiz veriyi "ezberlemesi" ve kendisini kapsamlı bir tahmin edici yapamamasıdır.Bunun önüne geçmek için ridge regresyonunda bir penalty(ceza) terimi bulunur.

$$L = \sum_{i=1}^n(y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^p(W_j)^2$$

bu loss function da başındaki En Küçük Kareler dışında $$\color{red}\lambda \sum_{j=1}^{p} (W_j)^2$$ terimi bulunur buna L2 cezası denir ve modeldeki tüm katsayıların(örneğin basit doğrusal regresyonda $\beta_1$ bir katsayıydı) toplamının lambda değeri ile çarpılmasıdır. Burada lambda bizim kontrol ettiğimiz bir hiperparametredir ve modelin nasıl öğreneceğini belirler.

## Hiperparametre optimizasyonu yöntemleri

Bu blog yazısında 3 farklı hiperparametre optimizasyon yönteminden bahsedeceğiz.

1. Grid Search
2. Random Search
3. Bayesian Optimization
   
### Grid Search

Hiperparametrelerin belirli bir değer aralığında tüm kombinasyonlarının denenerek en iyi kombinasyonun bulunmasını sağlayan bir yöntemdir. Bu yöntem, kapsamlıdır ancak zaman alıcıdır.

### Random Serch

Hiperparametrelerin belirli bir değer aralığında tüm kombinasyonlarının denenmesi yerine verilen sayı kadar rastgele kombinasyonları değerlendirir ve en iyisini seçer. Bu yöntem daha az kapsamlıdır ancak modelin fazla hiperparametresi varsa grid searchten çok daha hızlıdır.

### Grid Search vs Random Serch

Örneğin bir Decision Tree(Karar Ağacı) algoritmasının 4 tane hiperparametresini optimize etmek istiyoruz ve aşağıdaki belirli değerlerin iyi olabileceğini düşünüyoruz.

'n_estimators': [100, 200, 300, 400]\
'max_depth': [None, 5, 10, 15, 20]\
'min_samples_split': [2, 5, 10]\
'min_samples_leaf': [1, 2, 4]

Bu değerler üzerine Grid Search yaparsak Grid Search'ün deneyeceği 4x5x3x3'ten toplam 180 tane kombinasyon vardır ve eklenen her bir hiperparametre değeri başına bu sayının çok daha fazla büyüyeceğini göz önüne alalım. Tüm kombinasyonları denemek yerine Random Search ile örneğin 25 tane kombinasyonu deneyebiliriz. Bu sayede zamandan ve hesaplama gücünden kazanırız ancak en iyi hiperparametre kombinasyonunu yakalayamayabiliriz. 

### Bayesian Optimization (Bayes optimizasyonu)


## Veri seti üzerinde örnek bir uygulama

![](/images/hyperparameter-blog/grid_search_cross_validation.png "Cross validation şeması")
