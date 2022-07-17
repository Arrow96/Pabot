"""“ChatbotBrain.py” importa las librerías necesarias y crea que clase “ChatbotBrain” que se utilizara para
la creación de la inteligencia artificial a utilizar en el proyecto. """
from chatterbot import  ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement

class ChatbotBrain:
    """El método “__init__()” cumple la función de constructor de la clase “ChatbotBrain()”, posee sus
    respectivos atributos, algunos con valores predeterminados que pueden ser modificados según se vea
    necesario. """
    def __init__(self):

        self.chatbot = ChatBot(
                'Pabot',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database='./db_chatbot.sqlite3',  # fichero de la base de datos (si no existe se creará automáticamente)
                logic_adapters=[

                    {
                        'import_path': "chatterbot.logic.BestMatch",
                        'statement_comparison_function': 'chatterbot.comparisons.levenshtein.distance'
                    },
                    {
                        'import_path': "chatterbot.logic.BestMatch",
                        'default_response': 'Lo siento, pero no entiendo' ,
                        'maximum_similarity_threshold': 0.90
                    }
                ],
                input_adapter='chatterbot.input.TerminalAdapter',  # indica que la pregunta se toma del terminal
                output_adapter='chatterbot.output.TerminalAdapter',  # indica que la respuesta se saca por el terminal

                preprocessors=[
                    'chatterbot.preprocessors.clean_whitespace'
                ],
            )
        self.context = ['Hola', 'Hola', '¿Como estas?', 'Estoy bien, gracias por preguntar']
        self.levenshtein_distance = LevenshteinDistance('es')

        self.error = Statement('No entiendo lo que dices')  # convertimos una frase en un tipo statement
        self.error2 = Statement('¿Puedes repetir lo que acabas de decir?')

    """El método “talk()” toma una variable de tipo string, manipula esta variable para que la inteligencia 
    artificial genere una repuesta que después será retornada. """
    def talk(self, ask):

        trainer = ListTrainer(self.chatbot)
        response = self.chatbot.get_response(ask)
        if self.levenshtein_distance.compare(Statement(ask), self.error) > 0.51 or response == 'Lo siento, pero no entiendo':
            response = '¿Qué debería haber dicho?'
        elif self.levenshtein_distance.compare(Statement(ask), self.error2) > 0.51 or response == 'Repite lo que acabas de decir, porfavor':
            response = f'{self.context[-1]}'
        elif(self.context[-1] == '¿Qué debería haber dicho?'):
            response = f'Entiendo, cuando digas: {self.context[-4]} debo responder: {ask}'
            trainer.train([self.context[-4], ask])

        self.context.append(ask)
        self.context.append(response)
        return response

