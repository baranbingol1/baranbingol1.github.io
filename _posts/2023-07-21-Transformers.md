# Transformerların yapısı ve HuggingFace kütüphanesi kullanımı

Merhabalar! İlk blog yazıma hoşgeldiniz. Bu yazıda ChatGPT'ninde altında bulunan Transformerları (hayır film serisi olan değil) anlamaya çalışacağız ayrıca HuggingFace kütüphanesine de giriş yapacağız.
Bu blog yazısı aslında uzun zamandır yazmayı planladığım bir yazı. Umarım okuyanlara faydalı olur!

Başlamadan önce bu yazıda üstünden geçeceklerimizi özetlemek gerekirse:

- Transformerların Kısa Tarihi
- RNN ve LSTM Yapıları
- Encoder-Decoder Yapısı
- Attention Yapısı
- ULMFiT
- HuggingFace ile Kullanım Örnekleri

## Transformerların Kısa Tarihi

"Transformer" yapısı ilk defa 2017 yılında Google Research Team'in yarattığı etkiye göre görece ciddiyetsiz bir başlığa sahip olan ["Attention Is All You Need"](https://arxiv.org/abs/1706.03762) makalesiyle dünyaya tanıtıldı.  
Bu yapının en önemli özelliği, RNN ve LSTM gibi klasik NLP algoritmalarının kullandığı sıralı işleme mekanizması yerine "dikkat" mekanizmasını etkili bir şekilde kullanıyor olması.
Dikkat mekanizması olan "Attention"ın yapısının ve Transformerlardaki yerinin ne olduğunu anlamadan önce karşılaştırabilmek için Transformerlardan önce sıklıkla kullanılan NLP yapılarını, RNN ve LSTM'leri anlamak lazım.

## RNN ve LSTM Yapıları

Recurrent Neural Network (RNN):

Bir roman okurken nasılki bulunduğunuz sayfadaki bilgileri anlamak için önceki sayfadaki bilgileri hatırlıyorsanız RNN yapılarıda buna benzer bir hatırlama yapısı ile çalışır. 
Bunu yapay sinir ağı içerisinde kendini tekrarlayan bir katman oluşturarak sağlar.
Bu katman aslında yapay sinir ağlarında input ile output katmanlarının arasında bulunan "gizli" dediğimiz katmanlara benzer. Tek farkı aynı zamanda bu katmanın bir sonraki RNN katmanı için input olmasıdır.
RNN'ler ismindende anlayabileceğimiz üzere(recurrent yani tekrarlayan) aslında katmanlarından biri kendini tekrar eden yapay sinir ağlarıdır.

![](/images/RNNvsNN.png "RNN vs Klasik Sinir Ağı Karşılaştırması")

RNN yapısının "vanishing gradient"(bkz: [Vanishing gradient problem](https://en.wikipedia.org/wiki/Vanishing_gradient_problem)) problemi vardır bu problem uzun paragraflardaki kelimeler arası ilişkileri anlamada sıkıntı çıkarır ayrıca çok hafıza kullandıklarından yavaş eğitilirler.

Long Short-Term Memory(LSTM):

LSTM'ler RNN'lerin en büyük problemlerinden biri olan vanishing gradient problemini çözer. LSTM'ler daha iyi hafıza sistemine sahip olan geliştirilmiş RNN'ler olarak düşünülebilir.
RNN'ler kısa hafıza gerektiren problemlerde örneğin bir cümlenin duygu analizi gibi sadece birkaç kelime arasında bağlantı kurmamız gereken problemlerde kullanılabilir.
LSTM'ler ise bir paragrafı özetlemek gibi daha fazla hafıza isteyen problemlerde kullanılabilir.
Tabii işin pratiğinde ikisi arasında bir seçim yapmak gerekirse LSTM'ler çoğu zaman RNN'lerden daha iyi performans verir.

{% include info.html text="RNN'ler ve LSTM'ler bu hatırlama yapıları sayesinde sadece doğal dil işleme değil aynı zamanda önceki verilere bağlı olan problemlerde yani zaman-serisi problemlerinde(ör: bir şehrin gelecek ay kullanacağı toplam su miktarını tahmin etme) de kullanılır." %}

## Encoder-Decoder Yapısı

Encoder-Decoder:

Encoder, girdi verilerini(örneğin bir metni) sayılarla temsil edeceği bir "last hidden state"e gönderir. Bu state daha sonrasında decoder içine girer ve bize çıktımızı verir.

![](/images/encoder-decoder-basit-ornek.PNG "Basit bir TR-EN çevirisi, encoder-decoder örneği")

Bu yapı oldukça basit ve sade olsada eksikliği vardır. 
Encoder kendi içinde birden fazla RNN katmanıyla girdi sözcüklerini birbirleriyle anlamdırabilse bile Decoder yapısına bir state halinde bilgileri ulaştırması gerekir buda bilgi kaybına yol açar.
Örneğin cümlenin başında geçen bir kelime cümlenin sonundaki bir kelimeyle bağlantılı olsa bile encoder bu bilgiyi veremeyebilir. Şanslıyiz ki bu problemi çözebilen Attention yapısı var.

## Attention Mekanizması

Encoder-Decoder yapısının ana eksikliğinin bilgi kaybı olduğundan bahsetmiştik.
Decoder'a tek bir input vermek yerine, Encoder'un her bir outputunu input olarak vermek güzel bir çözüm gibi duruyor.
Attention yapısı ise bu inputlardan hangisinin daha öncelikli olduğunu belirleyen ağırlıklar koyar ve Decoderda bu ağırlıklara göre outputunu oluşturur.

![](/images/attention-mekanizmasi.PNG "Attention Mekanizması")

Attention mekanizması her bir adımda(Decoderun oluşturacağı her yeni kelimede) hangi input ağırlıklarının daha önemli olduğunu değerlendirerek bize kelimeler arasında bir anlam(context) sağlar.
Bu yapının daha paralel bir şekilde gidebilmesi için Transformer makalesinde ise self-attention tanıtılıyor. Orijinal transformer yapısında encoder ve decoderların kendi attention mekanizmaları var ve attention outputları bir FFNN(feed forward neural network, klasik sinir ağı yapısı) yapısına gidiyor.
Böylece daha hızlı ve efektif bir şekilde modelleri eğitebiliyoruz.

![](/images/transformer-arch.png "Makaledeki Transformer Yapısı")

Transformer yapısının tam hali yukarıdaki resimde. Şu ana kadar konuştuklarımızın yanı sıra bu yapıda her katmanda bir "residual connection" ve normalization katmanları da var(resimdeki add & norm katmanları). Residual connectionlar(artık bağlantı) bir katmanın girdilerini oluşturduğu çıktılarada ekleyerek kendisinden sonraki katmana hem girdilerini hem de çıktılarını vererek ilerlemesini sağlıyor. Bu yapı ilk defa görüntü işleme algoritması olan ResNet'lerde karşımıza çıkıyor ve transformerlarda dahil birçok yerde kullanılıyor. Bu artık bağlantılar RNN'lerinde bir problemi olan vanishing gradient problemini çözer, modeli daha kolay eğitebilmemizi sağlar ve modelin performansını artırır. Birde normalization katmanlarını görüyoruz bu katman ise verinin çıktılarını normalize ederek daha stabil bir model eğitme süreci sağlar ayrıca overfitting gibi sorunların önüne geçer.

## ULMFiT

NLP dünyasındaki gelişmelerin önünü açan bir başka önemli makale ise [ULMFiT](https://arxiv.org/abs/1801.06146). ULMFiT(Universal Language Model Fine-tuning) makalesi NLP'de o zamana kadar oluşmayan bir transfer learning standardı sağladı.

{% include info.html text="Transfer learning: Başka veriler üzerinde eğitilen modelin(genellikle büyük veri setleri üzerinde eğitilen büyük modeller olurlar) eğitildiği veriye benzer başka veriler üzerinde tekrardan hiç değiştirilmeden veya kendi amacımız için biraz eğitilerek(buna fine-tuning denir genellikle sinir ağındaki son katmanın gerisindeki katmanlardaki ağırlıklara dokunmayarak son katmandaki ağırlıklar açılır ve model tekrardan eğitilir veya son katmandan sonra başka bir katman koyulur ve model tekrar eğitilir.) kullanılması." %}

![](/images/ulmfit-yaklasimi.png "ULMFiT Yaklaşımı")

Bu yaklaşım üç ana başlığa ayrılır.

Pretraining: Bir sonraki kelimeyi tahmin eden bir model oluşturur. Bunu oluşturmak oldukça kolaydır çünkü herhangi bir etiketleme yapmamız gerek yok ve ayrıca kolayca veri çekebileceğimiz Wikipedia gibi platformlar var.

Domain Adaptation(Alana uyarlama): Şimdiki görevimiz ise istediğimiz alana bu modeli uyarlamak. Wikipedia textlerinde eğittimiz modele IMDb film eleştirilerinin textlerini veriyoruz ve tekrardan sonraki kelimeyi bulması için eğitiyoruz.

Fine tuning: Bu aşamada ise model başka işler yapabilmesi için fine-tune edilir. Örneğin bir classification katmanı koyulur girilen imdb yorumunun pozitif mi negatif mi olduğu bulunur.

## HuggingFace ile Kullanım Örnekleri

Bu nispeten yeni NLP gelişmelerini ve gelecek olan NLP gelişmelerini deneyebilmek için en iyi library belkide HuggingFace çok kolay bir kullanımı var(birkaç satırla model deneyebiliyoruz!) ayrıca zengin bir model hub'ı var.
Bu örnekleri denemek istiyorsanız Google Colab veya Kaggle gibi ortamların notebooklarında denemenizi öneririm.

```python
# IMDb üzerinde bulduğum The Flash filmine gelen bir yorum
text = """
I always start any review of a superhero movie by making it clear that these are not my types of movies and my opinion, for any superfans out there, should always be taken with a grain of salt. 
Now with that in mind, I have to say 'The Flash' is about as much as I can enjoy one of these types of movies. 
This was a very fun ride I'm happy to admit.
The movie is basically fan-service on overdrive.
Anything a mega-fan has always wanted to see is likely going to show up at some stage in this movie. 
If that's your kind of thing then you are going to be in heaven.
I found the pacing good. 
The movie is just short of 2 and a half hours but that time goes by pretty quickly. 
As usual in these types of superhero movies I found the final battle scene the weakest the film had to offer. 
It got messy and convoluted and it was really the one part of the movie where I lost interest.
Of all the superhero movies I've seen this is probably the one least focused on the villain.
He really does feel like an after-thought more than anything. 
The movie is far more about Barry Allen and his mission. 
Which makes it surprising to me just how much I enjoyed the film, because the one thing I do often get out of these films is enjoyment from the villain.
I think people are going to have a good time with this one.
It doesn't feel like the usual copy and paste template that the MCU has been throwing out for 15 years now and it is certainly a step up from everything non-Batman that DC has been doing recently.
I really enjoyed this. 8/10.
"""
```

Şimdi sentiment analysis(duygu analizi) yapmak için basit bir "pipeline" oluşturalım. 

```python
# İstediğimiz modeli burda belirtebiliriz default olarak şuanlık [distilbert](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) kullanıyor
from transformers import pipeline

classifier = pipeline('text-classification')
```

```python
outputs = classifier(text)
print(outputs)
```

    [{'label': 'POSITIVE', 'score': 0.7585893869400024}]

Aynı zamanda question-answering de yapabiliriz

```python
qa_pipe = pipeline("question-answering")
q = "Did the person who write this enjoyed the movie ?"
outputs = qa_pipe(question=q, context=text)
print(outputs)
```

    {'score': 0.2294749617576599, 'start': 1510, 'end': 1538, 'answer': 'I really enjoyed this. 8/10.'}

Uzun bir yazıyı özetlemesini istiyorsak 'summarization'da kullanabiliriz.

```python
sum_pipe = pipeline('summarization')
outputs = sum_pipe(text)
print(outputs)
```

    [{'summary_text': " 'The Flash' is about as much as I can enjoy one of these types of superhero movies . The movie is basically fan-service on overdrive . It doesn't feel like the usual copy and paste template that the MCU has been throwing out for 15 years ."}]

Bunlar buzdağının sadece görünen kısmının ufak bir kısmı, daha fazlası için [HuggingFace NLP Tutorial](https://huggingface.co/learn/nlp-course/chapter0/1?fw=pt)

Benim bu yazıda anlatacaklarım bu kadar umarım yararlı olmuştur!
