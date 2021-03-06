# rest_framework imports
from psycopg2 import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # status has a list of status codes we can use in our Response
from rest_framework.exceptions import NotFound # not found is going to provide us with an exception that sends a 404 response to the end user

# custom imports
from .models import Exercise # model will be used to query the db
from .serializers.common import ExercisesSerializer
from .serializers.populated import PopulatedExercisesSerializer

# import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ExercisesListView(APIView):

  permission_classes = (IsAuthenticatedOrReadOnly, ) # one-tuple requires trailing comma

  # ENDPOINTS & METHODS
  # GET /exercises/
  # POST /exercises/
  
  #? GET - Returns all exercises
  def get(self, request):
    # in this controller, we just want to get all the items inside the exercises table and return it as a response
    exercises = Exercise.objects.all() # gets all the fields using the all() method
    # .all() returns a QuerySet, we need to use the serializer to convert this into a python datatype
    serialized_exercises = PopulatedExercisesSerializer(exercises, many=True) # if we expect multiple items in the QuerySet, use many=True
    print('Serialized Data ->', serialized_exercises)
    return Response(serialized_exercises.data, status=status.HTTP_200_OK) # Response() sends data and status back to the user as a response

  #? POST - Add a new exercise to the database
  def post(self, request):
    # to get the request body, we use the data key on the request object
    # this process of passing python into a serializer to convert to a QuerySet is known as deserialization
    deserialized_exercise = ExercisesSerializer(data=request.data)
    # serializers give us methods to check validity of the data being passed into the database
    # what this does is checks the model and makes sure it passes that validation
    # the method is is_valid() -> this raises an exception if it's not valid
    try:
      deserialized_exercise.is_valid()
      print(deserialized_exercise.errors)
      # if we get to this point then validation is passed
      # if is_valid() fails then we throw an exception
      deserialized_exercise.save()
      # if we get to this point the record has been saved
      # when saving, a data key is added to the exercises instance that contains a python copy of the record that has just been created
      return Response(deserialized_exercise.data, status.HTTP_201_CREATED)
    except Exception as e:
      print(type(e))
      print(e)
      return Response({'detail':str(e)}, status.HTTP_422_UNPROCESSABLE_ENTITY)



class ExercisesDetailView(APIView):

  permission_classes = (IsAuthenticatedOrReadOnly, )

  # Custom function
  # purpose of this function is to attempt to find a specific exercise, thus returning the exercise and throwing a 404 if it fails.
  def get_exercise(self, pk):
    try:
      # pk= is us detailing that we want to look in whatever column is the PRIMARY KEY column
      # the second pk is the captured value
      # this is the same as saying in SQL: WHERE id =1
      return Exercise.objects.get(pk=pk)
    except Exercise.DoesNotExist as e:
      print(e)
      raise NotFound({'detail':str(e)})

  # GET - return one item from the Exercises table
  def get(self, request, pk):
    exercise = self.get_exercise(pk)
    print('exercise ->', exercise)
    serialized_exercise = PopulatedExercisesSerializer(exercise)
    return Response(serialized_exercise.data, status.HTTP_200_OK)

  # PUT - update an exercise
  def put(self, request, pk):
    exercise_to_update = self.get_exercise(pk=pk)
    deserialized_exercise = ExercisesSerializer(exercise_to_update, request.data)
    try:  
      deserialized_exercise.is_valid()
      print(deserialized_exercise.errors)
      deserialized_exercise.save()
      return Response(deserialized_exercise.data, status=status.HTTP_202_ACCEPTED )
    except Exception as e:
      return Response({'detail': str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

  # DELETE - delete an exercise
  def delete(self, request, pk, format=None):
        exercise_to_delete = self.get_exercise(pk)
        exercise_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
