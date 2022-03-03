package edu.pucmm.eitc;


import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.core.DenseInstance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils;

import java.io.File;
import java.io.FileInputStream;
import java.util.Random;
import java.util.Scanner;

public class Main {
    private static NaiveBayes model;
    private static Instances data;
    private static Scanner scanner = new Scanner(System.in);
    private static String[] texto = {
            "Tiene pelo? Si(1), No(0)", "Tiene plumas? Si(1), No(0)", "Pone huvos? Si(1), No(0)", "Produce leche? Si(1), No(0)", "Puede volar? Si(1), No(0)",
            "Es acuatico? Si(1), No(0)", "Es un depredador? Si(1), No(0)", "Posee dientes? Si(1), No(0)", "Tiene columna? Si(1), No(0)", "Respira? Si(1), No(0)",
            "Es venenoso? Si(1), No(0)", "Tiene agallas? Si(1), No(0)", "Cuantas patas tiene?(Entre 0 y 9)", "Tiene cola? Si(1), No(0)", "Es un animal domesticable? Si(1), No(0)",
            "Tiene el tamaño de un gato? Si(1), No(0)"};

    private static String[] types = {"Mamifero","Pajaro","Reptil","Pez","Anfibio","Insecto","Invertebrado"};


    public static void main(String[] args) throws Exception {
        String path = "src/main/resources/zoo_model.model";
        File file = new File(path);
        String absolutePath = file.getAbsolutePath();
        model = (NaiveBayes) weka.core.SerializationHelper.read(absolutePath);
        data = new Instances(model.getHeader());

        printMenu();
    }

    public static void printMenu() throws Exception {
        int opt = 0;
        while (opt != 4){
            System.out.println("\n\n============Clasificador de animales============");
            System.out.println("1 - Clasificar un animal");
            System.out.println("2 - Ver clasificaciones anteriores");
            System.out.println("3 - Inspeccionar modelo");
            System.out.println("4 - Salir");
            System.out.println("\nIngrese la opccion deseada: ");
            opt = Integer.parseInt(scanner.next());

            switch (opt){
                case 1:
                    getData();
                    break;
                case 2:
                    inspectOldClassifications();
                    break;
                case 3:
                    inspectModel();
                    break;
                case 4:
                    break;
                default:
                    System.out.println("La opcion seleccionada es invalidad! Por favor, intentelo de nuevo");
                    System.out.println("==============================================");
                    break;
            }
        }

    }

    public static void getData() throws Exception {
        double[] instance = new double[data.numAttributes()];
        for(int i = 1; i < 17; i++){
            System.out.println(texto[i-1]);
            int val = Integer.parseInt(scanner.next());
            if(i != 13){
                if(val == 0 || val == 1){
                    instance[i] = val;
                }else{
                    i--;
                    System.out.println("Opcion no valida! Intentelo de nuevo");
                }
            }else{
                if(val >=0 && val <= 9){
                    instance[i] = val;
                }else{
                    System.out.println("Cantidad de patas invalidad! Por favor intentelo de nuevo");
                }
            }
        }
        convertToInstance(instance);
    }

    public static void convertToInstance(double[] instance) throws Exception {
        //Se crea una nueva instancia de peso 1 con los datos optenidos
        DenseInstance aux = new DenseInstance(1.0,instance);
        //Se agrega la instancia al data set
        data.add(aux);
        //Se indica que la clase a clasificar es el ultimo atributo de la instancia
        data.setClassIndex(data.numAttributes()-1);
        //Se utiliza el modelo para realizar la clasificacion, lo que devuelve un double que representa el id del tipo de animal
        int type = (int) model.classifyInstance(data.lastInstance());
        System.out.println("El animal es de tipo: " +  types[type]);
    }

    public static void inspectModel() throws Exception {
        ConverterUtils.DataSource auxData = new ConverterUtils.DataSource("zoo.arff");
        Instances trainDataset = auxData.getDataSet();
        trainDataset.setClassIndex(trainDataset.numAttributes()-1);

        NaiveBayes auxModel = new NaiveBayes();
        auxModel.buildClassifier(trainDataset);
        Evaluation eval = new Evaluation(trainDataset);

        eval.crossValidateModel(auxModel,trainDataset, 10,new Random(1));

        System.out.println(eval.toSummaryString());
        System.out.println(eval.toMatrixString());
    }

    public static void inspectOldClassifications(){
        if(data.numInstances() == 0){
            System.out.println("Todavía no se han realizado clasificaciones");
        }else{
            for(int i = 0; i < data.numInstances(); i++){
                System.out.println(data.get(i));
            }
        }
    }
}
