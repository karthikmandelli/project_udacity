# PROGRAMMER: John Paul Hunter
# DATE CREATED: Monday, January 16, 2023                                   
# REVISED DATE: 
# PURPOSE: train the model

import torch

def train_model(model, epochs, this_device, criterion, optimizer, train_dataloader, valid_dataloader):
# Train and Validate the Model
#epochs = EPOCHS
 steps = 0
 print_every = 5
 running_loss = 0

# work out available architecture
 this_arch = "cpu"
 if this_device:
    this_arch = "gpu"

# NB// by default, the model is set to "training" mode
 for epoch in range(epochs):
    for inputs, labels in train_dataloader:
        steps += 1
        # move the input and label tensors to this device (cpu or gpu if available)
        inputs, labels = inputs.to(this_arch), labels.to(this_arch)
        
        # get log probabilities from our model and pass in images
        logps = model.forward(inputs)

        # calculate the batch loss
        loss = criterion(logps, labels)
        
        # clear the gradients of all optimized variables
        optimizer.zero_grad()

        # do a backwards pass
        loss.backward()

        # perform a single optimization step (parameter update)
        optimizer.step()

        # keep track of training loss
        running_loss += loss.item()
        
        if steps % print_every == 0:
            # Keep track of training and validation loss
            validation_loss = 0
            accuracy = 0
            model.eval()
            with torch.no_grad():
                for inputs, labels in valid_dataloader:
                    inputs, labels = inputs.to(this_arch), labels.to(this_arch)
                    logps = model.forward(inputs)
                    
                    # update loss metrics
                    batch_loss = criterion(logps, labels)
                    validation_loss += batch_loss.item()
                    
                     # calculate accuracy
                    ps = torch.exp(logps)
                    top_p, top_class = ps.topk(1, dim=1)
                    equals = top_class == labels.view(*top_class.shape)
                    accuracy += torch.mean(equals.type(torch.FloatTensor)).item()
                    
            print(f"Epoch {epoch+1}/{epochs}.. "
                  f"Train loss: {running_loss/print_every:.3f}.. "
                  f"Validation loss: {validation_loss/len(valid_dataloader):.3f}.. "
                  f"Test accuracy: {accuracy/len(valid_dataloader):.3f}")
            running_loss = 0
            model.train()