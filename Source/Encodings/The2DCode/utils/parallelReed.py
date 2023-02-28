import time
import multiprocessing
import numpy as np
import reedSolomon


class parallelReed():
    #cores = 8
    #pool = None
    inner_encoder = None
    outer_encoder = None

    def __init__(self, inner_encoder, outer_encoder):
        self.inner_encoder = inner_encoder
        self.outer_encoder = outer_encoder
        # Count number of cpu cores
        #self.cores = multiprocessing.cpu_count()

        # create Pool
        # self.pool = multiprocessing.Pool(
        #    processes=(self.cores*4))

    def encodeInner(input_vec, encoder, pos, return_dict):
        output_vec = encoder.encode(input_vec)
        return_dict[pos] = output_vec

    def encodeOuter(input_vec, encoder, pos, return_dict):
        output_vec = encoder.encode(encoder.convert_to_symbol_array(input_vec))
        return_dict[pos] = encoder.symbol_array_to_array(output_vec)

    def decodeInner(input_vec, decoder, pos, return_dict):
        output_vec = decoder.decode(input_vec)
        return_dict[pos] = output_vec

    def decodeOuter(input_vec, decoder, pos, return_dict):
        output_vec = decoder.decode(decoder.convert_to_symbol_array(input_vec))
        return_dict[pos] = decoder.symbol_array_to_array(output_vec)

    def encode(self, inputList, return_dict):
        print(len(inputList))
        # start outer encode
        for x, block in enumerate(inputList):
            parallelReed.encodeOuter(
                block[119:713, 3:33].tolist(), self.outer_encoder, x, return_dict)
            # self.pool.apply(
            #    self.encodeOuter, (block[119:713, 3:33], self.outer_encoder, x, return_dict))

        # stop the pool at the end
        # self.pool.close()
        # self.pool.join()

        # fill in results
        for x, block in enumerate(inputList):
            block[0:119, 3:33] = return_dict.get(x)[594:713]

        return_dict.clear()

        # add the index
        index = [0, 0, 1]
        indexCount = 0
        for block in inputList:
            for column in block:
                column[0:3] = index
                indexCount += 1
                increaseIndex(index)
                # Test for wrong indecies in the decoding, test was succesfull
                # if ((indexCount % 713) == 223) or ((indexCount % 713) == 566):
                #    print("Skipped increase at:", indexCount)
                # elif ((indexCount % 713) == 224) or ((indexCount % 713) == 567):
                #    increaseIndex(index)
                #    increaseIndex(index)
                # else:
                #    increaseIndex(index)

        # start inner encode
        for x, block in enumerate(inputList):
            for y, column in enumerate(block):
                parallelReed.encodeInner(
                    column[0:33].tolist(), self.inner_encoder, ((x * 713) + y), return_dict)
                # self.pool.apply(self.encodeInner, (self, column,
                #                self.inner_encoder, x, return_dict))

        # stop the pool at the end
        # self.pool.close()
        # self.pool.join()

        # fill in results
        for x, block in enumerate(inputList):
            for y, column in enumerate(block):
                column[33:39] = return_dict.get((x * 713) + y)[33:39]

        return_dict.clear()

    def decode(self, inputList, return_dict):
        # start inner decode
        for x, block in enumerate(inputList):
            for y, column in enumerate(block):
                parallelReed.decodeInner(
                    column.tolist(), self.inner_encoder, ((x * 713) + y), return_dict)
                # self.pool.apply_async(func=parallelReed.decodeInner, args=(
                #    column, self.inner_encoder, x, return_dict))

        # stop the pool at the end
        # self.pool.close()
        # self.pool.join()

        # fill in results
        for x, block in enumerate(inputList):
            for y, column in enumerate(block):
                column[0:33] = return_dict.get((x * 713) + y)

        return_dict.clear()

        # sort columns
        # 1. create new blocks
        newList = []
        for x in range(0, len(inputList)):
            newList.append(np.zeros((713, 39), dtype=int))
        unusedColumns = []
        usedIndex = []

        # 2. put in columns on correct spot (sort & delete)
        for x, block in enumerate(inputList):
            for y, column in enumerate(block):
                index = (column[0] * 47) + (column[1] * 47) + column[2]

                # check if the pos is empty
                if index in usedIndex:
                    unusedColumns.append(column)
                else:
                    block = index // 713
                    pos = index % 713
                    if pos == 0:
                        pos = 712
                        block -= 1
                    else:
                        pos -= 1
                    if block > (len(inputList) - 1):
                        unusedColumns.append(column)
                    else:
                        newList[block][pos] = column
                        usedIndex.append(index)

        # 3. fill in unused rows
        # TODO test if we need that
        '''
        maxIndex = len(inputList) * 713
        listIndex = 0
        for index in range(0, maxIndex + 1):
            if index not in usedIndex:
                if listIndex < len(unusedColumns):
                    print("Filled at spot: ", index)
                    block = index // 713
                    pos = index % 713
                    if pos == 0:
                        pos = 712
                        block -= 1
                    else:
                        pos -= 1
                    newList[block][pos] = unusedColumns[listIndex]
                    listIndex += 1
                else:
                    break
        '''

        # start outer decode
        for x, block in enumerate(newList):
            parallelReed.decodeOuter(
                np.concatenate((block[119:713, 3:33], block[0:119, 3:33])).tolist(), self.outer_encoder, x, return_dict)
            # self.pool.apply_async(func=parallelReed.encodeOuter, args=(
            #    block[119:713, 3:33], self.outer_encoder, x, return_dict))

        # stop the pool at the end
        # self.pool.close()
        # self.pool.join()

        # fill in results
        for x, block in enumerate(inputList):
            block[119:713, 3:33] = return_dict.get(x)

        return_dict.clear()

    # Input should be a list of arrays with array-size (713x39)
    def startRsCode(self, inputList, codingType):
        start_time = time.time()  # TODO remove the time

        # create manager/dict for return values
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        if(codingType == 0):
            self.encode(inputList, return_dict)
        else:
            self.decode(inputList, return_dict)

        print("--- %s seconds ---" %
              (time.time() - start_time))  # TODO remove the time


def increaseIndex(index):
    index[2] += 1
    if(index[2] >= 47):
        index[2] = 0
        index[1] += 1
        if(index[1] >= 47):
            index[1] = 0
            index[0] += 1
            if(index[0] >= 47):
                index[2] = 0
                index[1] = 0
                index[0] = 0
                raise ValueError("Index was to big, file needs to be smaller.")
