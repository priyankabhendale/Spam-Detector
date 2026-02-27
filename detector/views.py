from django.shortcuts import render
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from .forms import MessageForm

dataset = pd.read_csv("emails.csv")

# ---- Load dataset ----


# ---- Vectorize ----
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(dataset['text'])
y = dataset['spam']

# ---- Split ----
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---- Train model ----
model = MultinomialNB()
model.fit(x_train, y_train)


def predictMessage(message):
    messageVector = vectorizer.transform([message])
    prediction = model.predict(messageVector)
    return 'Spam' if prediction[0] == 1 else 'Ham'


def Home(request):
    result = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['text']
            result = predictMessage(message)
    else:
        form = MessageForm()

    return render(request, 'home.html', {
        'form': form,
        'result': result
    })
