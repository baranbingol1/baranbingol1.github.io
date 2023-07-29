# Feature Selection(Özellik Seçimi) Nedir ve Örnek Bir Uygulaması

Merhaba, bu yazıda makine öğrenmesi modelleri için özellik seçimi yapmayı(örneğin 50 sütunu olan verisetini özellik seçimi yaparak sütun sayısını 30'a indirmek) bir örnek üzerinde göreceğiz.\
Özellik seçimi verinin sahip olduğu özellikleri(sütun sayısı) ihtiyacımıza göre seçmektir.

## Neden Özellik Seçimi 

* Modeli basitleştirmek istememiz böylece model daha anlaşılır olacaktır.
* Modelin performansını arttırmak.
* Modelin çalışma hızını arttırmak.
* [Curse of Dimensionality](https://en.wikipedia.org/wiki/Curse_of_dimensionality): Verideki özellik sayısı arttıkça veri toplamanın zorlaşması, modelin isabet oranını arttırmak için daha fazla veri gerekmesi, [overfitting](https://en.wikipedia.org/wiki/Overfitting)'in daha da olası olması ve veriyi görselleştirmenin daha da zorlaşması.(50 boyutlu bir veriyi görselleştirmeye çalıştığınızı düşünün)

## Özellik Seçimi Metotları

* **Filter methods**: Bu methodlarda özellik seçimi istatistiksel yollarla olur. Kategorik veriler için Chi-square test yapılabilir ya da daha genel olarak Correlation-ranking yapılabilir bu yöntemde tahmin etmek istediğimiz özellik ile diğer özelliklerin korelasyonuna göre özellik seçimi yapılır.
* **Wrapper methods**: Veri özelliklerine göre alt kümelere ayrılır ve modelin performansı ölçülür buna göre özellik seçimi yapılır. Forward selection yapabiliriz bu methodda boş bir kümeyle başlanır ve özellikler eklenmeye başlanır etkilerine göre özellik seçimi yapılır. Backward elimination yönteminde verideki tüm özellikler ile başlanır ve özellikler tek tek silinerek etkileri gözlemlenir, en az etkisi olan özellikler silinir. Recursive Feature Elimination(RFE) yönteminde ise verinin tüm özellikleriyle model eğitilir belli bir kritere göre(coefficients, importance score gibi) en az önemi olan özellikler silinir. Bu iterasyon belirlenen özellik sınırına ulaşana kadar devam eder.
* **Embedded methods**: Bu methodlarda ise özellik seçimi algoritması kullanılan makine öğrenmesi algoritmasının içinde zaten vardır. LASSO(Least Absolute Shrinkage and Selection Operator): Modelin loss fonksiyonuna bir "ceza" ekler. Böylece modelde bazı özelliklerin katsayısı 0'a yakın olur. Ridge: Buda LASSO'ya benzer ama eklediği "ceza" terimi farklıdır. Random-Forest, Gradient Boosting Machines gibi ağaç tabanlı makine öğrenmesi algoritmalarının içinde feature selection bulunur.


## Methodların Avantajları ve Dezavantajları

* Filter methods: hızlı ve efektiflerdir ancak bazen alakasız özellikleri öne çıkarabilirler ayrıca target ile seçilen özellik arasındaki ilişkiyi dikkate aldığından özellikler arasındaki ilişkiyi dikkate almaz.
* Wrapper methods: Özellikler arasındaki ilişki dikkate alınır ancak bu methodların uygulanması fazla zaman alır.
* Embedded methods: Özellikler arasındaki ilişkiyi dikkate alır ayrıca hızlıdır ancak dezavantajı ise her makine öğrenmesi algoritmasında bulunamamasıdır.

## Feature Selection Örneği

Feature Selection'ın birkaç uygulamasını görmek için kaggle da oluşturduğum notebooka göz atabilirsiniz.
https://www.kaggle.com/code/baranbingl/feature-selection-nedir-nas-l-yap-l-r/

"Talk is cheap. Show me the code." - Linus Torvalds
