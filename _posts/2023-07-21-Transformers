# Transformerların yapısı ve HuggingFace kütüphanesi kullanımı

Merhabalar! İlk blog yazıma hoşgeldiniz. Bu yazıda ChatGPT'ninde altında bulunan Transformerları (hayır film serisi olan değil) anlamaya çalışacağız ayrıca HuggingFace kütüphanesine de giriş yapacağız.
Bu blog yazısı aslında uzun zamandır yazmayı planladığım "Transformerlar ile NLP" serisinin ilk postu. Umarım okuyanlara faydalı olur!

Başlamadan önce bu yazıda üstünden geçeceklerimizi özetlemek gerekirse:

- Transformerların Kısa Tarihi
- RNN ve LSTM Yapıları
- Encoder-Decoder ve Attention Yapıları
- Transformerlar ile Neler Yapabiliriz
- HuggingFace ile Kullanım Örnekleri

## Transformerların Kısa Tarihi

"Transformer" yapısı ilk defa 2017 yılında Google Research Team'in yarattığı etkiye göre görece ciddiyetsiz bir başlığa sahip olan "Attention Is All You Need" makalesiyle dünyaya tanıtıldı.  
Bu makalenin başlığından da anlayabileceğimiz üzere en önemli kısmı yeni ve alışılagelmişin dışında olan "Attention" yapısının tanıtılması.
Bu yapının en önemli özelliği, RNN ve LSTM gibi klasik NLP algoritmalarının kullandığı sıralı işleme mekanizması yerine "dikkat" mekanizmasını kullanıyor olması.
Dikkat mekanizması olan "Attention"ın yapısının ne olduğunu anlamadan önce karşılaştırabilmek için Transformerlardan önce kullanılan NLP yapılarını, RNN ve LSTM'leri anlamak lazım.

## RNN ve LSTM Yapıları

Recurrent Neural Network (RNN):

Bir roman okurken nasılki bulunduğunuz sayfadaki bilgileri anlamak için önceki sayfadaki bilgileri hatırlıyorsanız RNN yapılarıda buna benzer bir hatırlama yapısı ile çalışır. 
Bunu yapay sinir ağı içerisinde bir "hidden state" katmanı oluşturarak sağlar. Peki nedir bu hidden state katmanı ?
Hidden state katmanı aslında yapay sinir ağlarında ortada bulunan "gizli" dediğimiz katmanlara benzer. Tek farkı aynı zamanda bu katmanın bir sonraki RNN katmanı için input olmasıdır.
Yani RNN'lerin ismindende anlayabileceğimiz üzere(recurrent yani tekrarlayan) aslında katmanlarından biri kendini tekrar eden yapay sinir ağlarıdır.

![](/images/RNNvsNN.png "RNN vs Klasik Sinir Ağı Karşılaştırması (Kaynak: k21academy)")

RNN yapısının "vanishing gradient"(bkz: [Vanishing gradient problem](https://en.wikipedia.org/wiki/Vanishing_gradient_problem)) buda uzun paragraflardaki kelimeler arası ilişkileri anlamada sıkıntı çıkarır ayrıca çok hafıza kullandıklarından yavaş eğitilirler.

Long-Short Term Memory(LSTM):

LSTM'ler RNN'lerin en büyük problemlerinden biri olan vanishing gradient problemini çözer. LSTM'ler daha iyi hafıza sistemine sahip olan geliştirilmiş RNN'ler olarak düşünülebilir.
RNN'ler kısa hafıza gerektiren problemlerde örneğin bir cümlenin duygu analizi gibi sadece birkaç kelime arasında bağlantı kurmamız gereken problemlerde kullanılabilir.
LSTM'ler ise bir paragrafı özetlemek gibi daha fazla hafıza isteyen problemlerde kullanılabilir.
Tabii işin pratiğinde ikisi arasında bir seçim yapmak gerekirse LSTM'ler çoğu zaman RNN'lerden daha iyi performans verir.

{% include info.html text="RNN'ler ve LSTM'ler bu hatırlama yapıları sayesinde sadece doğal dil işleme değil aynı zamanda önceki verilere bağlı olan problemlerde yani zaman-serisi problemlerinde(ör: bir şehrin gelecek ay kullanacağı toplam su miktarını tahmin etme) de kullanılır." %}

